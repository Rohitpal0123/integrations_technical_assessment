from datetime import datetime
from typing import Optional

class IntegrationItem:
    def __init__(
        self,
        id: Optional[str] = None,
        city: Optional[str] = None,
        company: Optional[str] = None,
        email: Optional[str] = None,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        phone: Optional[str] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None,
    ):
        self.id = id
        self.city = city
        self.company = company
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.createdAt = createdAt
        self.updatedAt = updatedAt
