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

The backbone network is used for transfer learning and feature extraction. For Body Pose estimation, a pre-trained VGG (Oxford Visual Geometry Group) network is used. The backbone network generates a set of feature maps that is input into the model for inference.

    K. Simonyan and A. Zisserman. Very deep convolutional networks for large-scale image recognition. In ICLR, 2015.

## Confidence Maps and Part Affinity Fields

The model produces a set of confidence maps (heatmaps) and part affinity fields. Each confidence map is a 2D representation of the confidence that a keypoint appears to a particular pixel. In an image, the confidence peaks where the keypoint is visible.

![heatmap1](%placeholder2a%)
![heatmap2](%placeholder2b%)

Part affinity fields address the problem of associating each detected body part to full-body poses of each person in the image. Given a set of detected keypoints, part affinity fields measure the association of each pair of body part detections. In essence, part affinity fields are 2D vector fields representing each limb, which encodes the direction that points from one part of the limb to the other.

![paf1](%placeholder2c%)
![paf2](%placeholder2d%)

## Multistage Refinement

After the initial set of part affinity fields and confidence maps are produced, the part affinity fields are first refined by using the image feature maps. Subsequently, the confidence maps are refined in a similar manner. The resultant part affinity fields and confidence maps are then parsed in the following step.

## Results

Non-maximum suppresion is applied on the confidence maps to obtain a set of candidate part locations. With these candidate parts, a set of candidate limbs are derived and scored using the part affinity fields. Bipartite graph matching is applied on the candidate parts and limbs to parse the full-body pose for each person in the image.

%placeholder3%

![placeholder4](%placeholder4%)
