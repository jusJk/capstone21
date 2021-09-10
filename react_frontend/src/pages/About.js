import { useState } from 'react';
// material
import { Container, Stack, Typography } from '@material-ui/core';
// components
import Page from '../components/Page';
import { ProductList } from '../components/dashboard/products';

// ----------------------------------------------------------------------

export default function About() {
  return (
    <Page title="About">
      <Container>
        <Typography variant="h4" sx={{ my: 5 }}>
          This website is free software, licensed under the MIT license. It is made with Slave
          Labour from the National University of Singapore.
        </Typography>
      </Container>
    </Page>
  );
}
