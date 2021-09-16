// material
import { styled } from '@material-ui/core/styles';
import { Link as RouterLink } from 'react-router-dom';
import { Button, Card, Grid, Typography } from '@material-ui/core';
// components
import Page from '../components/Page';

// ----------------------------------------------------------------------
const RootStyle = styled(Card)(({ theme }) => ({
  boxShadow: 'none',
  textAlign: 'left',
  padding: theme.spacing(5, 4),
  // color: theme.palette.info.darker,
  // backgroundColor: theme.palette.info.lighter
  color: theme.palette.primary.lighter,
  background: `linear-gradient(
          rgba(0, 0, 0, 1),
          rgba(0, 0, 0, 1)
        ), url(
    'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/book-quotes-1531945007.jpg?crop=1.00xw:0.753xh;0,0.247xh&resize=1200:*'
  )`,
  backgroundSize: 'cover'
}));

const RootStyleAbout = styled(Card)(({ theme }) => ({
  boxShadow: 'none',
  textAlign: 'left',
  padding: theme.spacing(5, 4),
  color: theme.palette.info.darker,
  backgroundColor: theme.palette.info.lighter
}));

const RootStyleNVIDIA = styled(Card)(({ theme }) => ({
  boxShadow: 'none',
  textAlign: 'left',
  padding: theme.spacing(5, 4),
  // color: theme.palette.info.darker,
  // backgroundColor: theme.palette.info.lighter
  color: theme.palette.info.lighter,
  background: `linear-gradient(
          rgba(0, 0, 0, 1),
          rgba(0, 0, 0, 1)
        ), url(
    'https://developer-blogs.nvidia.com/wp-content/uploads/2020/12/triton.png'
  )`,
  backgroundSize: 'cover'
}));

export default function Landing() {
  return (
    <Page title="Home" sx={{ marginLeft: '10%', marginTop: '3%' }}>
      <Grid container spacing={3}>
        <Grid item md={12} sx={{ padding: '2%' }}>
          <Typography variant="h1">Welcome!</Typography>
          ST Engineering's AI-as-a-Service platform powered by NVIDIA AI Toolkit
        </Grid>
        <Grid item md={12}>
          <Typography variant="h5">Getting Started</Typography>
        </Grid>

        <Grid item md={5}>
          <RootStyle>
            <Typography variant="h3">Model Catalog</Typography>
            <Grid container spacing={3}>
              <Grid item md={10}>
                Browse available models - test them with custom images, view model performance, and
                learn about underlying model design/architecture.
              </Grid>
              <Grid item>
                <Button variant="contained" component={RouterLink} to="/catalog/">
                  <Typography variant="subtitle1">Go</Typography>
                </Button>
              </Grid>
            </Grid>
          </RootStyle>
        </Grid>
        <Grid item md={3}>
          <RootStyleNVIDIA>
            <Typography variant="h3">Resources</Typography>
            <Grid container spacing={3}>
              <Grid item md={9}>
                Learn about NVIDIA's AI Toolkit that powers this platform
              </Grid>
              <Grid item>
                <Button variant="contained" color="secondary" href="https://ngc.nvidia.com/">
                  <Typography variant="subtitle1">Go</Typography>
                </Button>
              </Grid>
            </Grid>
          </RootStyleNVIDIA>
        </Grid>
        <Grid item md={3}>
          <RootStyleAbout>
            <Typography variant="h3">About</Typography>
            <Grid container spacing={3}>
              <Grid item>
                This platform was built by students from the National University of Singapore (NUS).
              </Grid>
            </Grid>
          </RootStyleAbout>
        </Grid>
      </Grid>
    </Page>
  );
}
