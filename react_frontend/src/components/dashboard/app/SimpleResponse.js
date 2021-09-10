// material
import { React, useState } from 'react';
import { styled } from '@material-ui/core/styles';
import { Card, CardContent, Typography, Stack, Button, Box } from '@material-ui/core';
// utils

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function SimpleResponse() {
  return (
    <Card
      variant="outlined"
      sx={{ m: '2%', borderRadius: '10px', boxShadow: 'none', textAlign: 'left' }}
    >
      <CardContent>
        <Typography variant="h5" component="h2">
          Response
        </Typography>
        <Typography>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
          sit amet blandit leo lobortis eget.
        </Typography>
      </CardContent>
    </Card>
  );
}
