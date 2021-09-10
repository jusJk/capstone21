// material
import { React, useState } from 'react';
import { styled } from '@material-ui/core/styles';
import {
  Divider,
  Card,
  Grid,
  CardContent,
  Alert,
  Typography,
  Stack,
  Button,
  Box,
  ButtonGroup,
  ButtonGroupContent
} from '@material-ui/core';
// utils

import { sendPostRequest } from '../../../../API/component';
// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
const ImgStyle = styled('img')({
  top: 0,
  maxWidth: '20vw',
  margin: '4%',
  marginLeft: '1%',
  alignItems: 'center',
  borderRadius: '25px'
});

export default function UploadPicture(props) {
  const [imgSrc, setImgSrc] = useState('');
  const [uploadFile, setUploadFile] = useState({});
  const [content, setContent] = useState('');

  const _onChange = function (e) {
    const file = e.target.files[0];
    const url = URL.createObjectURL(file);
    setImgSrc(url);
    setUploadFile(file);
  };

  const handleFormUpload = function () {
    const formData = new FormData();
    formData.append('file', uploadFile);
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    };
    sendPostRequest(
      props.api.endpoint,
      formData,
      (e) => {
        setContent(JSON.stringify(e));
      },
      config
    );
  };
  return (
    <Card
      variant="outlined"
      sx={{ m: '2%', borderRadius: '10px', boxShadow: 'none', textAlign: 'left' }}
    >
      <CardContent>
        <Stack direction="row">
          <Typography variant="h5" component="h2">
            {props.api.name}
          </Typography>
        </Stack>
        <Divider sx={{ my: '1%' }} />
        <Box>
          <Box>
            {content === '' ? null : (
              <Alert sx={{ m: '1.5%' }} severity="info">
                {content}
              </Alert>
            )}
          </Box>
          <Grid container justify>
            {imgSrc ? (
              <Stack>
                <Typography variant="subtitle1">File Preview:</Typography>
                <ImgStyle src={imgSrc} alt="" />
              </Stack>
            ) : null}
          </Grid>

          <ButtonGroup>
            <Button variant="text" component="label" color="info" size="large">
              Upload Picture
              <input
                type="file"
                hidden
                onChange={(e) => {
                  _onChange(e);
                }}
              />
            </Button>
            <Button
              variant="text"
              component="label"
              color="info"
              size="large"
              disabled={!imgSrc}
              onClick={() => {
                handleFormUpload();
              }}
            >
              Submit
            </Button>
          </ButtonGroup>
          <Box flex="1" />
        </Box>
      </CardContent>
    </Card>
  );
}
