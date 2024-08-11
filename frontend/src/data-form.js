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
  console.log("integrationType", integrationType);

  const handleLoad = async () => {
    try {
      const formData = new FormData();
      formData.append("credentials", JSON.stringify(credentials));
      const response = await axios.post(
        `http://localhost:8000/integrations/${endpoint}/load`,
        formData
      );
      const data = response.data;
      console.log("🚀 ~ data:", data);
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
      sx={{ padding: "20px" }}
    >
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        width="100%"
        maxWidth="800px"
        sx={{ mb: 2 }}
      >
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
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>ID</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>First Name</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Last Name</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Phone Number</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>City</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Company Name</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Created At</TableCell>
                  <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f5f5f5", borderBottom: "1px solid #ddd" }}>Updated At</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loadedData.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>{item.id || "N/A"}</TableCell>
                    {console.log(loadedData)}
                    <TableCell>{item.firstname || "N/A"}</TableCell>
                    <TableCell>{item.lastname || "N/A"}</TableCell>
                    <TableCell>{item.email || "N/A"}</TableCell>
                    <TableCell>{item.phone || "N/A"}</TableCell>
                    <TableCell>{item.city || "N/A"}</TableCell>
                    <TableCell>{item.company || "N/A"}</TableCell>
                    <TableCell>{item.createdAt || "N/A"}</TableCell>
                    <TableCell>{item.updatedAt || "N/A"}</TableCell>
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
