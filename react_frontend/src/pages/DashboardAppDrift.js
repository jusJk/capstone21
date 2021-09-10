// material
import { Box, Paper, Stack, Grid, Container, Typography } from '@material-ui/core';
import { styled } from '@material-ui/core/styles';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import DashboardSidebar from '../layouts/dashboard/DashboardSidebar';

import { AppWebsiteVisits } from '../components/dashboard/app';

import { getModelDetails } from '../API/component';

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1.5),
  textAlign: 'center',
  color: theme.palette.text.secondary
}));

export default function DashboardAppInference(props) {
  const [modelInfo, setModelInfo] = useState({});
  const id = useParams();
  useEffect(() => {
    setModelInfo(getModelDetails(id.id));
  }, [id]);
  return (
    <Page title="Model Dashboard">
      <DashboardSidebar id={id.id} />
      <Container maxWidth="lg" sx={{ ml: '20%', mt: '2%' }}>
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
