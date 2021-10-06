import { Stack, Container, Typography } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Page from '../components/Page';
import { getModelDetails } from '../API/component';

// ----------------------------------------------------------------------

export default function DashboardAppContact() {
  const [modelInfo, setModelInfo] = useState({});
  const id = useParams();
  useEffect(() => {
    getModelDetails(id.id, setModelInfo);
    console.log(modelInfo);
  }, [id]);
  return (
    <Page title="Model Dashboard">
      {/* <DashboardSidebar id={id.id} /> */}
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Stack>
          <Typography variant="h2" sx={{ mb: '1%' }}>
            Contact
          </Typography>
          <Typography sx={{ mb: '1%' }}>
            Contact the maintainers of {id.id} ({modelInfo.model_name})
          </Typography>

          <Stack>
            <Typography sx={{ mb: '1%' }}>
              Email: <b>{modelInfo.email}</b>
            </Typography>
            <Typography sx={{ mb: '1%' }}>
              Phone: <b>{modelInfo.phone}</b>
            </Typography>
          </Stack>
        </Stack>
      </Container>
    </Page>
  );
}
