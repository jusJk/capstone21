import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { APIEndPoint } from '../components/dashboard/app';
import Page from '../components/Page';
import { getMd, getAvailableDemo } from '../API/component';
import { Markdown } from '../components/dashboard/markdown/markdownRenderer';

// ----------------------------------------------------------------------

export default function DashboardAppEx() {
  const [exMarkdown, setExMarkdown] = useState('');
  const [demoEndpoint, setDemoEndpoint] = useState(false);
  const id = useParams();

  useEffect(() => {
    getAvailableDemo(id.id, (e) => setDemoEndpoint(e.explainability_demo_api));
  }, [id]);

  useEffect(() => {
    getMd(`${id.id}/${id.id}_explainability.md`, setExMarkdown);
  }, [id.id]);

  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">Model Explainability</Typography>
        </Box>
        <Box sx={{ marginBottom: '3%' }}>
          {demoEndpoint ? <APIEndPoint key={id} api={demoEndpoint} /> : null}
        </Box>

        <Markdown markdown={exMarkdown} id={id.id} />
      </Container>
    </Page>
  );
}
