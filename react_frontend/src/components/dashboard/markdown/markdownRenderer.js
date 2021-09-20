import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { styled } from '@material-ui/core/styles';
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
  margin: '1%',
  alignItems: 'center',
  borderRadius: '25px'
});

const Image = (props) => <ImgStyle {...props} />;

export function Markdown({ infoMarkdown, id, ...others }) {
  return (
    <ReactMarkdown
      children={infoMarkdown}
      transformImageUri={(link) => linkhandler(link, id)}
      components={{ img: Image }}
      remarkPlugins={[remarkGfm]}
    />
  );
}
