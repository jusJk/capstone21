// material
import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import DashboardSidebar from '../layouts/dashboard/DashboardSidebar';
import { getModelDetails } from '../API/component';

// ----------------------------------------------------------------------

export default function DashboardApp(props) {
  const [modelInfo, setModelInfo] = useState({});
  const id = useParams();
  useEffect(() => {
    setModelInfo(getModelDetails(id.id));
  }, [id]);
  return (
    <Page title="Model Dashboard">
      <DashboardSidebar id={id.id} />
      <Container maxWidth="lg" sx={{ ml: '20%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">
            <b>{modelInfo.name}</b>
          </Typography>
          <Typography>
            Model ID: <b>{id.id}</b>
          </Typography>
        </Box>
        <Grid container spacing={3}>
          <Grid item sx={{ whiteSpace: 'pre-line' }}>
            <Typography variant="h3">Information</Typography>
            <Typography variant="p">{modelInfo.info}</Typography>
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
