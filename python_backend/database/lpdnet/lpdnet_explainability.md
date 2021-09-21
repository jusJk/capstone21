# Explainability - LPD Net

LPD Net is based on DetectNet_v2. In DetectNet, training data samples are larger images that contain multiple objects. For each object in the image the training label must capture not only the class of the object but also the coordinates of the corners of its bounding box.

Because the number of objects can vary between training images, a naive choice of label format with varying length and dimensionality would make defining a loss function difficult.

DetectNet solves this key problem by introducing a fixed 3-dimensional label format that enables DetectNet to ingest images of any size with a variable number of objects present. The DetectNet data representation is inspired by the representation used by [Redmon et al. 2015].

## Example

![test image](detectnet_data.png)

The DetectNet architecture has five parts specified in the Caffe model definition file. There are 3 important processes.

1. Data layers ingest the training images and labels and a transformer layer applies online data augmentation.
2. A fully-convolutional network (FCN) performs feature extraction and prediction of object classes and bounding boxes per grid square.
3. Loss functions simultaneously measure the error in the two tasks of predicting the object coverage and object bounding box corners per grid square.
