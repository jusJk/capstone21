import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Stack, Grid, Container, Typography } from '@material-ui/core';
import Page from '../components/Page';
import { AppWebsiteVisits } from '../components/dashboard/app';
import { getModelDetails } from '../API/component';

export default function DashboardAppPerf() {
  const id = useParams();
  const [chart, setChart] = useState();
  useEffect(() => {
    getModelDetails(id.id, (e) => {
      setChart(e.stats);
    });
  }, [id]);

  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Stack>
          <Typography variant="h2" sx={{ mb: '1%' }}>
            Model Performance
          </Typography>
          <Typography variant="p">This is how the model performs over time</Typography>
        </Stack>
        {chart === undefined ? null : (
          <Grid container spacing={3} sx={{ mt: '1%' }}>
            <Grid item xs={12} md={12}>
              <AppWebsiteVisits
                xvalues={chart.performance.x}
                yvalues={chart.performance.y}
                title="Model Performance"
              />
            </Grid>
          </Grid>
        )}
      </Container>
    </Page>
  );
}
