import PropTypes from 'prop-types';
import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Card, Link, Typography, Stack } from '@material-ui/core';
import { styled } from '@material-ui/core/styles';
import Label from './Label';
import { getImageUrl } from '../../../API/component';

// ----------------------------------------------------------------------

const ProductImgStyle = styled('img')({
  top: 0,
  width: '100%',
  height: '100%',
  objectFit: 'cover',
  position: 'absolute'
});

// ----------------------------------------------------------------------

ShopProductCard.propTypes = {
  product: PropTypes.object
};

export default function ShopProductCard({ product }) {
  const { name, cover, status, id } = product;
  const [coverUrl, setCoverUrl] = useState();
  useEffect(() => {
    getImageUrl(cover, setCoverUrl);
  }, [id]);
  return (
    <Card>
      <Box sx={{ pt: '100%', position: 'relative' }}>
        {status && (
          <Label
            variant="filled"
            color={(status === 'development' && 'error') || 'info'}
            sx={{
              zIndex: 9,
              top: 16,
              right: 16,
              position: 'absolute',
              textTransform: 'uppercase'
            }}
          >
            {status}
          </Label>
        )}
        <ProductImgStyle alt={name} src={coverUrl} />
      </Box>

      <Stack spacing={2} sx={{ p: 3 }}>
        <Link
          to={{ pathname: `/dashboard/app/info/${id}` }}
          color="inherit"
          underline="hover"
          component={RouterLink}
        >
          <Typography variant="subtitle2" noWrap>
            {name}
          </Typography>
        </Link>
      </Stack>
    </Card>
  );
}
