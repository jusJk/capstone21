// material
import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';

import Page from '../components/Page';

import { APIEndPoint } from '../components/dashboard/app';

// ----------------------------------------------------------------------

export default function DashboardApp() {
  const id = useParams();

  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">Model Explainability</Typography>
        </Box>
        <Typography variant="h6" sx={{ mb: '1%' }}>
          Start by uploading an image:
        </Typography>
        <APIEndPoint
          api={{
            type: 'POST',
            body_type: 'image',
            name: 'Image Model Explainability',
            endpoint: `api/${id.id}/`
          }}
        />
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
