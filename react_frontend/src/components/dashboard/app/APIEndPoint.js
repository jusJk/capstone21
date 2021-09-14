// material
import { React, useState } from 'react';
import { styled } from '@material-ui/core/styles';
import { Card, CardContent, Typography, Stack, Button, Box } from '@material-ui/core';
import { ImageRequest, TextRequest, PlaceholderRequest } from '.';
// utils

// ----------------------------------------------------------------------
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

const getJsonCard = function (api) {
  return <TextRequest api={api} />;
};

const postImageCard = function (api) {
  return <ImageRequest api={api} />;
};

const placeholderCard = function (api) {
  return <PlaceholderRequest api={api} />;
};
// ----------------------------------------------------------------------

export default function APIEndPoint({ api }) {
  const [tryButton, setTryButton] = useState(false);

  const RootStyle = styled(Card)(({ theme }) => ({
    boxShadow: 'none',
    textAlign: 'left',
    padding: theme.spacing(3, 5),
    color: colorPicker(theme, api.type),
    backgroundColor: bgColorPicker(theme, api.type)
  }));

  const endPointTypeHandler = (api) => {
    const componentMap = {
      GET: { json: getJsonCard },
      DELETE: { json: placeholderCard },
      POST: { image: postImageCard }
    };
    const func = componentMap[api.type][api.body_type];
    console.log(func);
    if (func !== undefined) {
      return func(api);
    }
  };

  return (
    <>
      <RootStyle>
        <Stack direction="row" spacing={2}>
          <Typography variant="h4">{api.type}</Typography>
          <Typography variant="h4">{api.endpoint}</Typography>
          <Box flex={1} />
          <Button
            fullwidth
            variant="contained"
            color={buttonVariantPicker(api.type)}
            onClick={() => {
              setTryButton((old) => !old);
            }}
          >
            TRY IT OUT
          </Button>
        </Stack>
      </RootStyle>
      {tryButton && endPointTypeHandler(api)}
    </>
  );
}