import React from 'react';
import { Stack, Grid, Container, Typography, Skeleton, Box } from '@material-ui/core';
import Page from '../components/Page';
import { AppWebsiteVisits } from '../components/dashboard/app';

export default function DashboardAppDrift({ userProfile }) {
  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      {userProfile === 'Admin' ? (
        <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
          <Stack>
            <Typography variant="h2" sx={{ mb: '1%' }}>
              Model Drift
            </Typography>
          </Stack>
          <Box>
            <Skeleton />
            <Skeleton height={150} />
            <Skeleton />
            <Skeleton />
          </Box>
          <Grid container spacing={3} sx={{ mt: '1%' }}>
            <Grid item xs={12} md={12}>
              <AppWebsiteVisits />
            </Grid>
          </Grid>
        </Container>
      ) : (
        <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
          <Stack>
            <Typography variant="h4" sx={{ mb: '1%' }}>
              This is an admin page
            </Typography>
          </Stack>
        </Container>
      )}
    </Page>
  );
}
