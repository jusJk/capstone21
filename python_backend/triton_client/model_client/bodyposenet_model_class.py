import os

import requests
from requests.exceptions import ConnectionError

from base_model_class import BaseModelClass
from bodyposenet_client import bodyposenet_predict
from tao_triton.python.postprocessing.utils import plot_keypoints


class BodyPoseNetClass(BaseModelClass):

    def __init__(self, client_info):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        BaseModelClass.__init__(self, client_info)
        self._url = "35.240.147.255:6000"
        self._model_name = "bodyposenet"
        self._mode = "BodyPoseNet"

    def status(self):
        '''
        Returns the status of the model
        '''
        try:
            triton_server_url = "http://" + self._url + "/v2/health/ready"
            response = requests.get(triton_server_url)
        except ConnectionError as error:
            return {'HTTPStatus' : 503, 'status':'Inactive'}
        else:
            return {'HTTPStatus' : 200, 'status':'Active'}

    def predict(self, file_path):
        """Runs inference on images in file_path if it exists

        Args:
            file_path (string): File path of images to infer

        Returns:
            dict: If file path exists, returns dict containing results which stores the keypoints 
            detected for each image and skeleton edge names used for postprocessing.
            Else returns response indicating file path does not exist.
        """

        if os.path.exists(file_path):
            return self._predict(file_path)
        else:
            return {'HTTPStatus': 400,
                    'error': "File Path does not exist!"}

    def _predict(self, file_path):
        number_files = len([name for name in os.listdir(
            file_path) if os.path.isfile(file_path+name)])
        if number_files < 256:
            self._batch_size = 8
        else:
            self._batch_size = 32
        return bodyposenet_predict(model_name=self._model_name, mode=self._mode, url=self._url,
                                   image_filename=file_path, output_path='./', verbose=False, streaming=False, async_set=False,
                                   protocol='HTTP', model_version="", batch_size=self._batch_size)

if __name__ == '__main__':
    bp = BodyPoseNetClass(1)
    res = bp._predict('../input/bodyposenet')
    output = plot_keypoints(res, 'bp-sample.png', '../input/bodyposenet/bp-sample.png') # image with keypoints/limbs rendered
    # TODO: Save the image in correct output path

    import pickle
    with open('output.pickle', 'wb') as handle:
        pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)

