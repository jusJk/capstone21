// material
import { Stack, Grid, Container, Typography } from '@material-ui/core';

// components

import Page from '../components/Page';

import { AppWebsiteVisits } from '../components/dashboard/app';

export default function DashboardAppInference() {
  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Stack>
          <Typography variant="h2" sx={{ mb: '1%' }}>
            Model Performance
          </Typography>
          <Typography variant="p">
            Model drift is an important factor when using AI for business applications.
          </Typography>
        </Stack>
        <Grid container spacing={3} sx={{ mt: '1%' }}>
          <Grid item xs={12} md={12}>
            <AppWebsiteVisits />
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
