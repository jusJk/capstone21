import { getModels } from '../API/component';

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

const allModels = getModels();

const products = allModels.forEach((model, index) => {
  const setIndex = index + 1;
  console.log('index');

  return {
    id: index,
    cover: model.picture,
    name: model,
    status: model.status
  };
});

export default products;
