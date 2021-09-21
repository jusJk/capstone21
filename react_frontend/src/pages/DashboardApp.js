// material
import { Box, Grid, Container, Typography } from '@material-ui/core';
// components
import { useParams } from 'react-router-dom';

import { useState, useEffect } from 'react';
import Page from '../components/Page';
import { getModelDetails, getMd } from '../API/component';
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
    getMd(`${id.id}/${id.id}_info.md`, setInfoMarkdown);
  }, [id.id]);

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

        <Markdown markdown={infoMarkdown} id={id.id} />
      </Container>
    </Page>
  );
}
