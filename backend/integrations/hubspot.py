import datetime
import os
import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import hashlib
import requests
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis
from dotenv import load_dotenv

load_dotenv()

# HubSpot OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
AUTHORIZATION_URL = "https://app.hubspot.com/oauth/authorize"
TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"
scope = "crm.objects.contacts.read crm.objects.contacts.write"


async def authorize_hubspot(user_id, org_id):
    """
    Generates the authorization URL for HubSpot OAuth.

    Args:
        user_id (str): Unique identifier for the user.
        org_id (str): Unique identifier for the organization.

    Returns:
        str: Authorization URL to redirect the user to.
    """
    state_data = {
        "state": secrets.token_urlsafe(32),
        "user_id": user_id,
        "org_id": org_id,
    }
    encoded_state = base64.urlsafe_b64encode(
        json.dumps(state_data).encode("utf-8")
    ).decode("utf-8")

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "state": encoded_state,
        "response_type": "code",
    }

    auth_url = (
        AUTHORIZATION_URL
        + "?"
        + "&".join([f"{key}={value}" for key, value in params.items()])
    )

    await add_key_value_redis(
        f"hubspot_state:{org_id}:{user_id}", json.dumps(state_data), expire=600
    )

    return auth_url


async def oauth2callback_hubspot(request: Request):
    """
    Handles the OAuth2 callback from HubSpot and exchanges the code for an access token.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        HTMLResponse: Closes the authentication popup.
    """
    if request.query_params.get("error"):
        raise HTTPException(
            status_code=400, detail=request.query_params.get("error_description")
        )

    code = request.query_params.get("code")
    encoded_state = request.query_params.get("state")
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode("utf-8"))

    original_state = state_data.get("state")
    user_id = state_data.get("user_id")
    org_id = state_data.get("org_id")

    saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")

    if not saved_state or original_state != json.loads(saved_state).get("state"):
        raise HTTPException(status_code=400, detail="State does not match.")

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    token_data = response.json()
    await add_key_value_redis(
        f"hubspot_credentials:{org_id}:{user_id}",
        json.dumps(token_data),
        expire=600,
    )

    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)


async def get_hubspot_credentials(user_id, org_id):
    """
    Retrieves HubSpot credentials stored in Redis and deletes them after retrieval.

    Args:
        user_id (str): Unique identifier for the user.
        org_id (str): Unique identifier for the organization.

    Returns:
        dict: HubSpot credentials.
    """
    credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
    if not credentials:
        raise HTTPException(status_code=400, detail="No credentials found.")
    credentials = json.loads(credentials)
    print("credentials: ", credentials)
    await delete_key_redis(f"hubspot_credentials:{org_id}:{user_id}")
    return credentials


def create_integration_item_metadata_object(contact_json: dict) -> IntegrationItem:
    """
    Creates an IntegrationItem object from the HubSpot contact JSON.

    Args:
        contact_json (dict): JSON data of a HubSpot contact.

    Returns:
        IntegrationItem: An instance of IntegrationItem containing contact details.
    """
    properties = contact_json.get("properties", {})
    return IntegrationItem(
        id=contact_json.get("id"),
        city=properties.get("city"),
        company=properties.get("company"),
        email=properties.get("email"),
        firstname=properties.get("firstname"),
        lastname=properties.get("lastname"),
        phone=properties.get("phone"),
        createdAt=properties.get("createdate"),
        updatedAt=properties.get("lastmodifieddate"),
    )


async def get_items_hubspot(credentials: str) -> list[IntegrationItem]:
    """
    Fetches contacts from HubSpot and converts them to IntegrationItem objects.

    Args:
        credentials (str): HubSpot access token.

    Returns:
        list[IntegrationItem]: List of IntegrationItem objects.
    """
    credentials = json.loads(credentials)
    access_token = credentials["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    url = "https://api.hubapi.com/crm/v3/objects/contacts?properties=firstname,lastname,email,phone,city,company,createdate,lastmodifieddate"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve HubSpot data")

    contacts = response.json().get("results", [])
    return [
        create_integration_item_metadata_object(contact) for contact in contacts
    ]
