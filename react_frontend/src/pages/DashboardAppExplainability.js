import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { ImageRequest } from '../components/dashboard/app';

import Page from '../components/Page';
import { getMd, getAvailableDemo } from '../API/component';
import { Markdown } from '../components/dashboard/markdown/markdownRenderer';

// ----------------------------------------------------------------------

export default function DashboardAppExplainability() {
  const [exMarkdown, setExMarkdown] = useState('');
  const [demoEndpoint, setDemoEndpoint] = useState(false);
  const [showMarkdown, setShowMarkdown] = useState(true);
  const id = useParams();
  const handleExplainabilityDemo = (e) => {
    if (e.explainability_demo_api !== undefined) {
      setDemoEndpoint(e.explainability_demo_api);
      setShowMarkdown(false);
    }
  };

  useEffect(() => {
    getMd(`${id.id}/${id.id}_explainability.md`, setExMarkdown);
    getAvailableDemo(id.id, handleExplainabilityDemo, [id.id]);
  }, [id.id]);

  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 2 }}>
          <Typography variant="h2">Model Explainability</Typography>
        </Box>

        <Box sx={{ pb: 3 }}>
          {demoEndpoint ? (
            <Typography variant="subtitle">
              Using your own picture, dynamically explore and find out more about the steps required
              to produce predictions from {id.id}.
              <br />
              The explanations below will be populated with intermediate outputs derived from your
              picture once you upload it.
            </Typography>
          ) : null}
        </Box>

        <Box sx={{ marginBottom: '3%' }}>
          {demoEndpoint ? (
            <ImageRequest
              api={demoEndpoint}
              callback={(e) => {
                setExMarkdown(e.explain_markdown);
                setShowMarkdown(true);
              }}
            />
          ) : null}
        </Box>

        <Markdown markdown={exMarkdown} id={id.id} />
      </Container>
    </Page>
  );
}
