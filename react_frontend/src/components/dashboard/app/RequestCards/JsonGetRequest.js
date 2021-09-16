// material
import { React, useState } from 'react';
import PropTypes from 'prop-types';
import { Card, CardContent, Typography, Button, Box, Alert, Divider } from '@material-ui/core';
// utils
import { sendGetRequest } from '../../../../API/component';
// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function SimpleResponse(props) {
  const [content, setContent] = useState('');
  return (
    <Card
      variant="outlined"
      sx={{ m: '2%', borderRadius: '10px', boxShadow: 'none', textAlign: 'left' }}
    >
      <CardContent>
        <Typography variant="h5" component="h2">
          {props.api.input}
        </Typography>
        <Box>
          {content === '' ? null : (
            <Alert sx={{ m: '1.5%' }} severity="info">
              {content}
            </Alert>
          )}
        </Box>

        <Divider sx={{ my: '1%' }} />
        <Box>
          <Button
            onClick={() => {
              setContent(' ');
              sendGetRequest(props.api.endpoint, (e) => {
                setContent(JSON.stringify(e));
              });
            }}
          >
            {content === '' ? 'Send Get Request' : 'Send Again'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}

SimpleResponse.propTypes = {
  api: PropTypes.object
};
