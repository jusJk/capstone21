import { Paper, Stack, Container, Typography } from '@material-ui/core';
import { styled } from '@material-ui/core/styles';
import { useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Page from '../components/Page';
import { APIEndPoint } from '../components/dashboard/app';
import { getAvailableDemo } from '../API/component';

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1.5),
  textAlign: 'center',
  color: theme.palette.text.secondary
}));

export default function DashboardAppInference() {
  const [modelEndpoints, setModelEndpoints] = useState([]);
  const id = useParams();
  useEffect(() => {
    getAvailableDemo(id.id, (e) => setModelEndpoints(e.api));
  }, [id]);
  return (
    <Page title="Model Dashboard">
      <Container maxWidth="lg" sx={{ ml: '5%', mt: '2%' }}>
        <Stack>
          <Typography variant="h2" sx={{ mb: '1%' }}>
            Inference
          </Typography>
          {modelEndpoints.map((item) => (
            <Item key={item.id}>
              <APIEndPoint key={item.id} api={item} />
            </Item>
          ))}
        </Stack>
      </Container>
    </Page>
  );
}
