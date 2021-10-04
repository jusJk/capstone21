// material
import { React, useState } from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Alert,
  AlertTitle,
  Divider,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  LinearProgress
} from '@material-ui/core';
// utils
import { sendGetRequest } from '../../../../API/component';
// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function SimpleResponse(props) {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
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
          {loading ? <LinearProgress sx={{ m: '3%', height: '2vh', borderRadius: '5px' }} /> : null}
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
              setContent('');
              setLoading(true);
              sendGetRequest(props.api.endpoint, (e) => {
                if (props.hideResponse !== true) {
                  setContent(JSON.stringify(e, null, 2));
                } else {
                  setContent('Success');
                }
                setLoading(false);
                if (props.callback) {
                  props.callback(e);
                }
              });
            }}
          >
            {content === '' ? 'Send Get Request' : 'Send Again'}
          </Button>
        </Box>
        <Accordion
          disableGutters
          sx={{
            '&:before': {
              display: 'none'
            },
            marginLeft: '-1%'
          }}
        >
          <AccordionSummary>
            <Button variant="outlined">Python Code Sample</Button>
          </AccordionSummary>
          <AccordionDetails>
            <Alert severity="secondary">
              <p>import requests</p>
              <br />
              <p>
                response = requests.get( %BASEURL% + {`"${props.api.endpoint.slice(0, -8)}"`} +
                %ID%)
              </p>
              <p>print(response.json(), flush=True)</p>
            </Alert>
          </AccordionDetails>
        </Accordion>
      </CardContent>
    </Card>
  );
}

SimpleResponse.propTypes = {
  api: PropTypes.object
};
