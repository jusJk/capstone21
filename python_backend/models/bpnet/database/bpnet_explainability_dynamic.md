# Key Points

Human pose estimation is the computer vision task of estimating the configuration (‘the pose’) of the human body by localizing certain key points on a body within a video or a photo. This localization can be used downstream to predict if a person is standing, sitting, lying down, or doing some activity like dancing or jumping.

NVIDIA's BPNET is a fully convolutional model with architecture consisting of

    1. a backbone network (VGG)
    2. an initial estimation stage which does a pixel-wise prediction of confidence maps (heatmaps) and part affinity fields
    3. followed by multistage refinement (0 to N stages) on the initial predictions.

We will explore these steps in the sections below.

First, given the base image:

![placeholder1](%placeholder1%)

## Backbone Network

The backbone network is used for transfer learning and feature extraction. For Body Pose estimation, a pre-trained VGG (Oxford Visual Geometry Group) network is used.

    K. Simonyan and A. Zisserman. Very deep convolutional networks for large-scale image recognition. In ICLR, 2015.

## Confidence Maps and Part Affinity Fields

![heatmap1](%placeholder2a%)
![heatmap2](%placeholder2b%)
![paf1](%placeholder2c%)
![paf2](%placeholder2d%)

## Multistage Refinement

## Results

%placeholder3%

![placeholder4](%placeholder4%)
