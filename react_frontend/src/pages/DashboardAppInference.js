// material
import { Box, Paper, Stack, Grid, Container, Typography } from '@material-ui/core';
import { styled } from '@material-ui/core/styles';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import DashboardSidebar from '../layouts/dashboard/DashboardSidebar';

import { APIEndPoint } from '../components/dashboard/app';
import { getModelDetails, getAvailableDemo } from '../API/component';

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1.5),
  textAlign: 'center',
  color: theme.palette.text.secondary
}));

export default function DashboardAppInference(props) {
  const [modelInfo, setModelInfo] = useState({});
  const [modelEndpoints, setModelEndpoints] = useState([]);
  const id = useParams();
  useEffect(() => {
    setModelInfo(getModelDetails(id.id));
    setModelEndpoints(getAvailableDemo(id.id));
  }, [id]);
  return (
    <Page title="Model Dashboard">
      <DashboardSidebar id={id.id} />
      <Container maxWidth="lg" sx={{ ml: '20%', mt: '2%' }}>
        <Stack>
          <Typography variant="h2" sx={{ mb: '1%' }}>
            Inference
          </Typography>
          {modelEndpoints.map((item) => (
            <Item>
              <APIEndPoint api={item} />
            </Item>
          ))}

          {/* <Item>
            <APIEndPoint type="POST" endpoint={`${id.id}/model/predict`} />
          </Item>
          <Item>
            <APIEndPoint type="DELETE" endpoint={`${id.id}/model/nuke`} />
          </Item> */}
        </Stack>
      </Container>
    </Page>
  );
}
