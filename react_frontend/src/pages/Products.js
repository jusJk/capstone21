import { useState } from 'react';
// material
import { Container, Stack, Typography } from '@material-ui/core';
// components
import Page from '../components/Page';
import { ProductList } from '../components/dashboard/products';
import { getModels } from '../API/component';

// ----------------------------------------------------------------------

export default function Catalog() {
  const PRODUCTS = getModels();

  return (
    <Page title="Model Catalog">
      <Container>
        <Typography variant="h2" sx={{ my: 5 }}>
          Model Catalog
        </Typography>
        <ProductList products={PRODUCTS} />
      </Container>
    </Page>
  );
}
