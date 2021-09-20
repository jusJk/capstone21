# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Simple class to run post processing of Triton Inference outputs."""

import os

import numpy as np
from sklearn.cluster import DBSCAN as dbscan
from google.protobuf.text_format import Merge as merge_text_proto

from tao_triton.python.postprocessing.postprocessor_lprnet import Postprocessor
import tao_triton.python.proto.postprocessor_config_pb2 as postprocessor_config_pb2
from tao_triton.python.types import KittiBbox
from tao_triton.python.postprocessing.utils import (
    denormalize_bounding_bboxes,
    iou_vectorized,
    pool_context,
    render_image,
    thresholded_indices
)
from tao_triton.python.utils.kitti import write_kitti_annotation
 
class LprnetPostprocessor(Postprocessor):
    """Post processor for Triton outputs from a DetectNet_v2 client."""

    def __init__(self, batch_size, frames,
                 output_path, data_format, mapping_output_file):
        """Initialize a post processor class for a classification model.
        
        Args:
            batch_size (int): Number of images in the batch.
            frames (list): List of images.
            output_path (str): Unix path to the output rendered images and labels.
            data_format (str): Order of the input model dimensions.
                "channels_first": CHW order.
                "channels_last": HWC order.
            classes (list): List of the class names.
            postprocessing_config (proto): Configuration elements of the dbscan postprocessor.
            target_shape (tuple): Shape of the model input.
        """
        # self.pproc_config = load_clustering_config(postprocessing_config)
        # self.classes = classes
        self.output_names = ["tf_op_layer_ArgMax",
                             "tf_op_layer_Max"]
        # self.bbox_norm = [35., 35]
        self.offset = 0.5
        self.scale_h = 1
        self.scale_w = 1
        # self.target_shape = target_shape
        # self.stride = self.pproc_config.stride
        print(mapping_output_file)
        super().__init__(batch_size, frames, output_path, data_format, mapping_output_file)
        # Format the dbscan elements into classwise configurations for rendering.
        # self.configure()

    def apply(self, results, this_id, render=True):
        """Apply the post processing to the outputs tensors.
        
        This function takes the raw output tensors from the detectnet_v2 model
        and performs the following steps:

        1. Denormalize the output bbox coordinates
        2. Threshold the coverage output to get the valid indices for the bboxes.
        3. Filter out the bboxes from the "output_bbox/BiasAdd" blob.
        4. Cluster the filterred boxes using DBSCAN.
        5. Render the outputs on images and save them to the output_path/images
        6. Serialize the output bboxes to KITTI Format label files in output_path/labels.
        """

        output_array = {}
        this_id = int(this_id)
        #Mapping file which is specified as an argument when calling the function
        mapping_output_file = self.mapping_output_file
        for output_name in self.output_names:
            output_array[output_name] = results.as_numpy(output_name)
        # print(output_array)
        print(output_array)
        predictions = output_array["tf_op_layer_ArgMax"]
        confidence_score = output_array["tf_op_layer_Max"]
        #Reading mapping file and creating a dictionary for mapping
        with open(mapping_output_file) as f:
            lines = f.read().splitlines()
        mapping_dictionary = {k:v for k,v in enumerate(lines)}
        length_dict = len(mapping_dictionary)
        final_output = ''
        confidence_scores_indv_image = []
        #Performing Mapping
        prev_char = -1
        current_frame = self.frames[this_id-1] 
        filename = os.path.basename(current_frame._image_path)
        for key_counter in range(len(predictions[0])):
            key = predictions[0][key_counter]
            if (key != prev_char) & (key < length_dict):
                final_output+=mapping_dictionary[key]
                confidence_scores_indv_image.append(confidence_score[0][key_counter])
            prev_char = key

        return final_output, confidence_scores_indv_image, filename

        # #Creating final output file directory if it does not exist
        # current_frame = self.frames[this_id-1] 
        # filename = os.path.basename(current_frame._image_path)
        # output_label_file = os.path.join(
        #     self.output_path, "infer_labels",
        #     "{}.txt".format(os.path.splitext(filename)[0])
        # )

        # # output_image_file = os.path.join(
        # #     self.output_path, "infer_images",
        # #     "{}.jpg".format(os.path.splitext(filename)[0])
        # # )

        # if not os.path.exists(os.path.dirname(output_label_file)):
        #     os.makedirs(os.path.dirname(output_label_file))

        # # if not os.path.exists(os.path.dirname(output_image_file)):
        # #     os.makedirs(os.path.dirname(output_image_file))
        # # file_path = output_label_file + ""

        # #Creating text file for final output
        # print(output_label_file)
        # with open(output_label_file, 'w') as file:
        #     file.write(final_output)

        