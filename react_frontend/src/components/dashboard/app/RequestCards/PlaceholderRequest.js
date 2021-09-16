// material
import { React } from 'react';
import PropTypes from 'prop-types';
import { Divider, Card, CardContent, Typography, Stack } from '@material-ui/core';
// utils

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function PlaceHolderRequest(props) {
  return (
    <Card
      variant="outlined"
      sx={{ m: '2%', borderRadius: '10px', boxShadow: 'none', textAlign: 'left' }}
    >
      <CardContent>
        <Stack direction="row">
          <Typography variant="h5" component="h2">
            {props.api.input}
          </Typography>
        </Stack>
        <Divider sx={{ my: '1%' }} />
      </CardContent>
    </Card>
  );
}

PlaceHolderRequest.propTypes = {
  api: PropTypes.object
};
