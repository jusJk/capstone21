import ReactMarkdown from 'react-markdown';
import React from 'react';
import remarkGfm from 'remark-gfm';
import { styled } from '@material-ui/core/styles';
import { Grid, Typography } from '@material-ui/core';

import { getImageUrl } from '../../../API/component';

const linkhandler = (link, id) => {
  let imgUrl = '';
  getImageUrl(`database/${id}/${link}`, (e) => {
    imgUrl = e;
  });
  return imgUrl;
};
const ImgStyle = styled('img')({
  top: 0,
  maxWidth: '40vw',
  maxHeight: '50vh',
  margin: '1%',
  alignItems: 'center',
  borderRadius: '25px'
});

const Image = (props) => <ImgStyle {...props} />;

export function Markdown({ markdown, id, ...others }) {
  console.log(markdown);
  return (
    <Typography variant="p" sx={{ whiteSpace: 'pre-line' }}>
      <ReactMarkdown
        children={markdown}
        transformImageUri={(link) => linkhandler(link, id)}
        components={{ img: Image }}
        plugins={remarkGfm}
      />
    </Typography>
  );
}
