// material
import { Box, Grid, Container, Typography } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';

import { useState, useEffect } from 'react';
import Page from '../components/Page';
import { getModelDetails, getInfoMd as getMd, getImageUrl } from '../API/component';
import { Markdown } from '../components/dashboard/markdown/markdownRenderer';
// ----------------------------------------------------------------------

export default function DashboardApp() {
  const [modelInfo, setModelInfo] = useState({});
  const [infoMarkdown, setInfoMarkdown] = useState('');
  const id = useParams();
  useEffect(() => {
    getModelDetails(id.id, setModelInfo);
  }, [id]);

  useEffect(() => {
    getMd(modelInfo.information_md, setInfoMarkdown);
  }, [modelInfo]);

  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Box sx={{ pb: 5 }}>
          <Typography variant="h2">
            <b>{modelInfo.model_name}</b>
          </Typography>
          <Typography>
            Model ID: <b>{id.id}</b>
          </Typography>
        </Box>
        <Grid container spacing={3}>
          <Grid item sx={{ whiteSpace: 'pre-line' }}>
            <Markdown infoMarkdown={infoMarkdown} />
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
