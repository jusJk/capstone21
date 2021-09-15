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
          about
        </Typography>
      </Container>
    </Page>
  );
}
