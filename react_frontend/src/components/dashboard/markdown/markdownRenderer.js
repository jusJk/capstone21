import ReactMarkdown from 'react-markdown';
import React from 'react';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { styled } from '@material-ui/core/styles';
import { Table, Typography } from '@material-ui/core';

import { getImageUrl } from '../../../API/component';

const linkhandler = (link, id) => {
  let imgUrl = '';
  if (link) {
    getImageUrl(link, (e) => {
      imgUrl = e;
    });
  }
  console.log(imgUrl);
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
  return (
    <Typography variant="p" sx={{ whiteSpace: 'pre-line' }}>
      <ReactMarkdown
        children={markdown}
        transformImageUri={(link) => linkhandler(link, id)}
        components={{ img: Image }}
        plugins={remarkGfm}
        rehypePlugins={[rehypeRaw]}
        skipHtml="false"
      />
    </Typography>
  );
}
