# BP (Body Pose) Net

## Model Overview

The BodyPoseNet models described in this card are used for multi-person human pose estimation network, which aims to predict the skeleton for every person in a given input image which consists of keypoints and the connections between them. This follows a single shot bottom-up methodology and there is no need for a person detector. Hence, the compute does not scale linearly with the number of people in the scene. The pose / skeleton output is commonly used as input for applications like activity/gesture recognition, fall detection, posture analysis, among others.

The default model predicts 18 keypoints including nose, neck, right_shoulder, right_elbow, right_wrist, left_shoulder, left_elbow, left_wrist, right_hip, right_knee, right_ankle, left_hip, left_knee, left_ankle, right_eye, left_eye, right_ear, left_ear.

![test image](database/bpnet/cover.png)

## Model Architecture

This is a fully convolutional model with architecture consisting of:

    - a backbone network (like VGG)
    - an initial estimation stage that does a pixel-wise prediction of confidence maps (heatmaps) and part affinity fields
    - multistage refinement (0 to N stages) on the initial predictions.

## Training Algorithm

The training algorithm optimizes the network to minimize the loss on confidence maps (heatmaps) and part affinity fields for given image and ground truth pose labels.

## Reference

    Zhe Cao, Gines Hidalgo, Tomas Simon, Shih-En Wei, Yaser Sheikh (2017).
    Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields.
    In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition.

## Usage

Primary use case for this model is to detect human poses in a given RGB image. BodyPoseNet is commonly used for activity/gesture recognition, fall detection, posture analysis etc.

### Input

Network accepts H X W x 3 input. The images are pre-processed to handle normalization, resizing while maintaining the aspect ratio etc.

### Output

Network outputs two tensors: confidence maps (H1' x W1' x C) and part affinity fields (H2' x W2' x P). After NMS and bipartite graph matching, we obtain final results with M x N X 3

where

    N is the number of keypoints.
    M is the number of humans detected in the image.
    C is the number of confidence map channels - corresponds to number of keypoints + background
    P is the number of part affinity field channels - corresponds to the (2 x number of edges used in the skeleton)
    H1', W1' are the height and width of the output confidence maps respectively
    H2', W2' are the height and width of the output part affinity fields respectively
