// material
import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import DashboardSidebar from '../layouts/dashboard/DashboardSidebar';
import { getModelDetails } from '../API/component';
import { APIEndPoint } from '../components/dashboard/app';

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
          <Typography variant="h2">Model Explainability</Typography>
        </Box>
        <Typography variant="h6" sx={{ mb: '1%' }}>
          Start by uploading an image:
        </Typography>
        <APIEndPoint type="POST" endpoint={`${id.id}/model/infer`} />
        <Grid sx={{ mt: '5%' }}>
          <Box>
            <Skeleton />
            <Skeleton width="80%" height={150} />
            <Skeleton />
            <Skeleton />
          </Box>
        </Grid>
      </Container>
    </Page>
  );
}
