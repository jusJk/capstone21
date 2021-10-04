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

from contextlib import contextmanager
from copy import deepcopy
import logging
from multiprocessing import Pool
import os
import math

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from sklearn.cluster import DBSCAN as dbscan
from PIL import ImageDraw

from tao_triton.python.types import KittiBbox
from tao_triton.python.utils.kitti import write_kitti_annotation
import tritonclient.grpc.model_config_pb2 as mc

logger = logging.getLogger(__name__)


@contextmanager
def pool_context(*args, **kwargs):
    """Simple wrapper to get pool context with close function."""
    pool = Pool(*args, **kwargs)
    try:
        yield pool
    finally:
        pool.terminate()


def denormalize_bounding_bboxes(
    bbox_array, stride, offset,
    bbox_norm, num_classes,
    scale_w, scale_h,
    data_format, model_shape, frames,
    this_id
):
    """Convert bbox from relative coordinates to absolute coordinates."""
    boxes = deepcopy(bbox_array)
    if data_format == mc.ModelInput.FORMAT_NCHW:
        _, model_height, model_width = model_shape
    else:
        model_height, model_width, _ = model_shape
    scales = np.zeros(
        (boxes.shape[0], 4, boxes.shape[2], boxes.shape[3])
    ).astype(np.float32)
    for i in range(boxes.shape[0]):
        frame = frames[(this_id * boxes.shape[0] + i) % len(frames)]
        scales[i, 0, :, :].fill(float(frame.width/model_width))
        scales[i, 1, :, :].fill(float(frame.height/model_height))
        scales[i, 2, :, :].fill(float(frame.width/model_width))
        scales[i, 3, :, :].fill(float(frame.height/model_height))
    scales = np.asarray(scales).astype(np.float32)
    target_shape = boxes.shape[-2:]
    gc_centers = [
        (np.arange(s) * stride + offset)
        for s in target_shape
    ]
    gc_centers = [s / n for s, n in zip(gc_centers, bbox_norm)]
    for n in range(num_classes):
        boxes[:, 4*n+0, :, :] -= gc_centers[0][:, np.newaxis] * scale_w
        boxes[:, 4*n+1, :, :] -= gc_centers[1] * scale_h
        boxes[:, 4*n+2, :, :] += gc_centers[0][:, np.newaxis] * scale_w
        boxes[:, 4*n+3, :, :] += gc_centers[1] * scale_h
        boxes[:, 4*n+0, :, :] *= -bbox_norm[0]
        boxes[:, 4*n+1, :, :] *= -bbox_norm[1]
        boxes[:, 4*n+2, :, :] *= bbox_norm[0]
        boxes[:, 4*n+3, :, :] *= bbox_norm[1]
        # Scale back boxes.
        boxes[:, 4*n+0, :, :] = np.minimum(
            np.maximum(boxes[:, 4*n+0, :, :], 0),
            model_width
        ) * scales[:, 0, :, :]
        boxes[:, 4*n+1, :, :] = np.minimum(
            np.maximum(boxes[:, 4*n+1, :, :], 0),
            model_height
        ) * scales[:, 1, :, :]
        boxes[:, 4*n+2, :, :] = np.minimum(
            np.maximum(boxes[:, 4*n+2, :, :], 0),
            model_width
        ) * scales[:, 2, :, :]
        boxes[:, 4*n+3, :, :] = np.minimum(
            np.maximum(boxes[:, 4*n+3, :, :], 0),
            model_height
        ) * scales[:, 3, :, :]
    return boxes


def thresholded_indices(cov_array, num_classes, classes, cov_threshold):
    """Threshold out valid bboxes and extract the indices per class."""
    valid_indices = []
    batch_size, num_classes, _, _ = cov_array.shape
    for image_idx in range(batch_size):
        indices_per_class = []
        for class_idx in range(num_classes):
            covs = cov_array[image_idx, class_idx, :, :].flatten()
            class_indices = covs > cov_threshold[classes[class_idx]]
            indices_per_class.append(class_indices)
        valid_indices.append(indices_per_class)
    return valid_indices


def render_image(frame, image_wise_bboxes, output_image_file, box_color, linewidth=3):
    """Render images with overlain outputs."""
    image = frame.load_image()
    draw = ImageDraw.Draw(image)
    for annotations in image_wise_bboxes:
        class_name = annotations.category
        box = annotations.box
        outline_color = (box_color[class_name].R,
                         box_color[class_name].G,
                         box_color[class_name].B)
        if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
            draw.rectangle(box, outline=outline_color)
            for i in range(linewidth):
                x1 = max(0, box[0] - i)
                y1 = max(0, box[1] - i)
                x2 = min(frame.width, box[2] + i)
                y2 = min(frame.height, box[3] + i)
                draw.rectangle(box, outline=outline_color)
    image.save(output_image_file)


def return_bbox_info(frame, image_wise_bboxes):
    """Returns final Bbox with file name"""
    final_annotations = []
    for annotations in image_wise_bboxes:  # Looping through all bboxes detected in the image
        class_name = annotations.category
        box = annotations.box
        if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
            x1 = max(0, box[0])
            y1 = max(0, box[1])
            x2 = min(frame.width, box[2])
            y2 = min(frame.height, box[3])
            width = x2 - x1
            height = y2 - y1
            confidence_score = annotations.confidence
            indv_bbox = {}
            indv_bbox["bbox"] = [x1, y1, width, height]
            indv_bbox["confidence_score"] = confidence_score
            final_annotations.append(indv_bbox)

    return final_annotations


def iou_vectorized(rects):
    """
    Intersection over union among a list of rectangles in LTRB format.

    Args:
        rects (np.array) : numpy array of shape (N, 4), LTRB format, assumes L<R and T<B
    Returns::
        d (np.array) : numpy array of shape (N, N) of the IOU between all pairs of rects
    """
    # coordinates
    l, t, r, b = rects.T

    # form intersection coordinates
    isect_l = np.maximum(l[:, None], l[None, :])
    isect_t = np.maximum(t[:, None], t[None, :])
    isect_r = np.minimum(r[:, None], r[None, :])
    isect_b = np.minimum(b[:, None], b[None, :])

    # form intersection area
    isect_w = np.maximum(0, isect_r - isect_l)
    isect_h = np.maximum(0, isect_b - isect_t)
    area_isect = isect_w * isect_h

    # original rect areas
    areas = (r - l) * (b - t)

    # Union area is area_a + area_b - intersection area
    denom = (areas[:, None] + areas[None, :] - area_isect)

    # Return IOU regularized with .01, to avoid outputing NaN in pathological
    # cases (area_a = area_b = isect = 0)
    return area_isect / (denom + .01)


def plot_keypoints(results, image_filename, image_path, render_limbs=True):
    """Renders keypoints on input image

    Args:
        results (dict): Inference output from BodyPoseNet prediction
        image_filename ([type]): File name of image used during inference
        image_path (str): Path to input image
        render_limbs (bool): If true, render limb connections

    Returns:
        (numpy.ndarray): Image with keypoints and limb connections rendered
    """

    image_res = results['results'][image_filename]
    skeleton_edge_names = results['skeleton_edge_names']
    colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [
                  0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85], [0, 85, 85]]

    stickwidth = 1  # width of limb connections
    radius = 2  # radius of keypoint circles
    canvas = cv.imread(image_path)
    to_plot = cv.imread(image_path)
    for person in image_res:
        total = person['total']
        person = list(person.items())
        for i in range(total-2):  # exclude last 2 elements which are score and total keypoints
            center = person[i][1]
            cv.circle(canvas, (int(center[0]), int(
                center[1])), radius, colors[i], thickness=-1)
    to_plot = cv.addWeighted(to_plot, 0.3, canvas, 0.7, 0)

    if not render_limbs:
        return to_plot

    for person in image_res:
        # Each edge is a joint represented by tuple (keypoint_a, keypoint_b)
        for i, edge in enumerate(skeleton_edge_names):
            keypoint_a = edge[0]
            keypoint_b = edge[1]
            if keypoint_a in person and keypoint_b in person:  # If both keypoints were identified
                # Get the x coords of each keypoint
                X = (person[keypoint_a ][1], person[keypoint_b][1])
                # Get the y coords of each keypoint
                Y = (person[keypoint_a ][0], person[keypoint_b][0])
                cur_canvas = canvas.copy()
                mX = np.mean(X)
                mY = np.mean(Y)
                length = ((X[0] - X[1]) ** 2 + (Y[0] - Y[1]) ** 2) ** 0.5
                angle = math.degrees(math.atan2(X[0] - X[1], Y[0] - Y[1]))
                polygon = cv.ellipse2Poly((int(mY), int(mX)), (int(
                    length/2), stickwidth), int(angle), 0, 360, 1)
                cv.fillConvexPoly(cur_canvas, polygon, colors[i])
                canvas = cv.addWeighted(canvas, 0.4, cur_canvas, 0.6, 0)

    return canvas
