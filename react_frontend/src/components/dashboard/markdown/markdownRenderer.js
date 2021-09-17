import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { styled } from '@material-ui/core/styles';
import { getImageUrl } from '../../../API/component';

const linkhandler = (link) => {
  let imgUrl = '';
  getImageUrl(link, (e) => {
    imgUrl = e;
  });
  return imgUrl;
};
const ImgStyle = styled('img')({
  top: 0,
  maxWidth: '40vw',
  margin: '1%',
  alignItems: 'center',
  borderRadius: '25px'
});

const Image = (props) => <ImgStyle {...props} />;

export function Markdown({ infoMarkdown, ...others }) {
  return (
    <ReactMarkdown
      children={infoMarkdown}
      transformImageUri={linkhandler}
      components={{ img: Image }}
      remarkPlugins={[remarkGfm]}
    />
  );
}
