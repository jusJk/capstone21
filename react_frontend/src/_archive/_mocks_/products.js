import { useEffect } from 'react';
import { sample } from 'lodash';
import { getModels } from '../API/component';
// utils
import { mockImgProduct } from '../utils/mockImages';

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
