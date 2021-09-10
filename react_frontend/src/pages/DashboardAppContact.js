// material
import {
  Box,
  CardContent,
  Card,
  Paper,
  Stack,
  Button,
  Container,
  Typography
} from '@material-ui/core';
import { styled } from '@material-ui/core/styles';
// components
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Page from '../components/Page';
import DashboardSidebar from '../layouts/dashboard/DashboardSidebar';
import { getModelDetails } from '../API/component';

// ----------------------------------------------------------------------

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1.5),
  textAlign: 'center',
  color: theme.palette.text.secondary
}));

export default function DashboardAppContact(props) {
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
            Contact
          </Typography>
          <Typography sx={{ mb: '1%' }}>
            Contact the maintainers of {id.id} ({modelInfo.name})
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
