# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

6eaa918b-7a6b-4e66-a304-80b26028c67d
56025998-1924-4f3e-80ff-842855e38281

import { useState } from "react";
import { Box, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import axios from "axios";

const endpointMapping = {
  Notion: "notion",
  Airtable: "airtable",
  Hubspot: "hubspot",
};

export const DataForm = ({ integrationType, credentials }) => {
  const [loadedData, setLoadedData] = useState(null);
  const endpoint = endpointMapping[integrationType];
  console.log("integrationType", integrationType)

  const handleLoad = async () => {
    try {
      const formData = new FormData();
      formData.append("credentials", JSON.stringify(credentials));
      const response = await axios.post(
        `http://localhost:8000/integrations/${endpoint}/load`,
        formData
      );
      const data = response.data;
      console.log("🚀 ~ data:", data)
      setLoadedData(data);
    } catch (e) {
      alert(e?.response?.data?.detail);
    }
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      width="100%"
      sx={{ padding: '20px' }}
    >
      <Box display="flex" flexDirection="column" alignItems="center" width="100%" maxWidth="800px" sx={{ mb: 2 }}>
        <Button 
          onClick={handleLoad} 
          sx={{ mt: 2, minWidth: "150px" }} 
          variant="contained"
        >
          Load Data
        </Button>
        <Button
          onClick={() => setLoadedData(null)}
          sx={{ mt: 1, minWidth: "150px" }}
          variant="contained"
        >
          Clear Data
        </Button>
      </Box>

      {loadedData && (
        <Box
          sx={{
            mt: 4,
            width: "100%",
            maxWidth: "800px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            overflowX: "auto",
            mb: 2,
          }}
        >
          <TableContainer>
            <Table aria-label="integration items table">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>First Name</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>Last Name</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>Phone Number</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>City</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>Company Name</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loadedData.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>{item.first_name || "N/A"}</TableCell>
                    <TableCell>{item.last_name || "N/A"}</TableCell>
                    <TableCell>{item.email || "N/A"}</TableCell>
                    <TableCell>{item.phone_number || "N/A"}</TableCell>
                    <TableCell>{item.city || "N/A"}</TableCell>
                    <TableCell>{item.company_name || "N/A"}</TableCell>
                    <TableCell>{item.status || "N/A"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      <TextField
        label="Json Loaded Data"
        value={loadedData ? JSON.stringify(loadedData, null, 2) : ""}
        sx={{ mt: 2 }}
        InputLabelProps={{ shrink: true }}
        disabled
        multiline
        fullWidth
        minRows={6}
        variant="outlined"
      />
    </Box>
  );
};
