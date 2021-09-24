import { Box, Grid, Container, Typography, Skeleton } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import Page from '../components/Page';
import { getMd } from '../API/component';
import { Markdown } from '../components/dashboard/markdown/markdownRenderer';

// ----------------------------------------------------------------------

export default function DashboardAppEx() {
  const [exMarkdown, setExMarkdown] = useState('');
  const id = useParams();

  useEffect(() => {
    getMd(`${id.id}/${id.id}_explainability.md`, setExMarkdown);
  }, [id.id]);

  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">Model Explainability</Typography>
        </Box>
        <Markdown markdown={exMarkdown} id={id.id} />

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
