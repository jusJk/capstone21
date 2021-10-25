import { Box, Grid, Container, Typography, Stack } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Page from '../components/Page';
import { getModelDetails, getMd } from '../API/component';
import { Markdown } from '../components/dashboard/markdown/markdownRenderer';
import { AppWebsiteVisits } from '../components/dashboard/app';

export default function DashboardAppAdmin({ userProfile }) {
  const [modelInfo, setModelInfo] = useState({});
  const [infoMarkdown, setInfoMarkdown] = useState('');
  const id = useParams();
  useEffect(() => {
    getModelDetails(id.id, setModelInfo);
  }, [id]);

  useEffect(() => {
    getMd(`models/${id.id}/database/${id.id}_admin.md`, setInfoMarkdown);
  }, [id.id]);

  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      {userProfile === 'Admin' ? (
        <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
          <Stack>
            <Typography variant="h2" sx={{ mb: '1%' }}>
              Model Admin
            </Typography>
          </Stack>
          <Box>
            <Markdown markdown={infoMarkdown} id={id.id} />
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
