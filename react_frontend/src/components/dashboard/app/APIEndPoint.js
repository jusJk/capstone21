// material
import { React, useState } from 'react';
import { styled } from '@material-ui/core/styles';
import { Card, CardContent, Typography, Stack, Button, Box } from '@material-ui/core';
import { UploadPicture, SimpleResponse } from '.';
// utils

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function APIEndPoint({ type, endpoint }) {
  const [tryButton, setTryButton] = useState(false);

  const colorPicker = (theme, type) => {
    const colors = {
      GET: theme.palette.primary.darker,
      DELETE: theme.palette.error.darker,
      POST: theme.palette.info.darker
    };
    return colors[type];
  };
  const bgColorPicker = (theme, type) => {
    const colors = {
      GET: theme.palette.primary.lighter,
      DELETE: theme.palette.error.lighter,
      POST: theme.palette.info.lighter
    };
    return colors[type];
  };
  const buttonVariantPicker = (type) => {
    const colors = {
      GET: 'primary',
      DELETE: 'error',
      POST: 'info'
    };
    return colors[type];
  };
  const RootStyle = styled(Card)(({ theme }) => ({
    boxShadow: 'none',
    textAlign: 'left',
    padding: theme.spacing(3, 5),
    color: colorPicker(theme, type),
    backgroundColor: bgColorPicker(theme, type)
  }));

  return (
    <>
      <RootStyle>
        <Stack direction="row" spacing={2}>
          <Typography variant="h4">{type}</Typography>
          <Typography variant="h4">{endpoint}</Typography>
          <Box flex={1} />
          <Button
            fullwidth
            variant="contained"
            color={buttonVariantPicker(type)}
            onClick={() => {
              setTryButton((old) => !old);
            }}
          >
            TRY IT OUT
          </Button>
        </Stack>
      </RootStyle>
      {tryButton && (type === 'POST' ? <UploadPicture /> : <SimpleResponse />)}
    </>
  );
}
