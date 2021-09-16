// material
import { Box, Grid, Container, Typography } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import { getModelDetails } from '../API/component';

// ----------------------------------------------------------------------

export default function DashboardApp() {
  const [modelInfo, setModelInfo] = useState({});
  const id = useParams();
  useEffect(() => {
    getModelDetails(id.id, setModelInfo);
  }, [id]);
  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">
            <b>{modelInfo.model_name}</b>
          </Typography>
          <Typography>
            Model ID: <b>{id.id}</b>
          </Typography>
        </Box>
        <Grid container spacing={3}>
          <Grid item sx={{ whiteSpace: 'pre-line' }}>
            <Typography variant="h3">Information</Typography>
            <Typography variant="p">{modelInfo.information}</Typography>
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
