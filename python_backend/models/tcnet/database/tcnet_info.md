# Traffic Cam Net

## Model Overview

The model described in this card detects one or more physical objects from four categories within an image and returns a box around each object, as well as a category label for each object. The four categories of objects detected by this model are – car, persons, road signs and two-wheelers. **In this model, we will only focus on the car category of objects.**

## Model Architecture

These models are based on **NVIDIA DetectNet_v2** detector with **ResNet18** as feature extractor. This architecture, also known as **GridBox object detection**, uses bounding-box regression on a uniform grid on the input image. Gridbox system divides an input image into a grid which predicts four normalized bounding-box parameters (xc, yc, w, h) and confidence value per output class.

The raw normalized bounding-box and confidence detections needs to be post-processed by a clustering algorithm such as **DBSCAN** or **NMS** to produce final bounding-box coordinates and category labels. This is done by the image clients that the model catalog provides.

## Training Algorithm

The training algorithm optimizes the network to minimize the localization and confidence loss for the objects. The training is carried out in two phases. In the first phase, the network is trained with regularization to facilitate pruning. Following the first phase, we prune the network removing channels whose kernel norms are below the pruning threshold. In the second phase the pruned network is retrained. Regularization is not included during the second phase.

## Citations

    Redmon, J., Divvala, S., Girshick, R., Farhadi, A.: You only look once: Unified, real-time object detection. In: CVPR. (2016)
    Erhan, D., Szegedy, C., Toshev, A., Anguelov, D.: Scalable object detection using deep neural networks, In: CVPR. (2014)
    He, K., Zhang, X., Ren, S., Sun, J.: Deep Residual Learning for Image Recognition. In: CVPR (2015)

## Usage

Primary use case intended for this model is detecting cars in a color (RGB) image. The model can be used to detect cars from photos and videos by using appropriate video or image decoding and pre-processing.

### Input

For EU license plate

    - Color Images of resolution 960 X 544 X 3 (W x H x C)
    - Channel Ordering of the Input: NCHW, where
        - N = Batch Size,
        - C = number of channels (3),
        - H = Height of images (544),
        - W = Width of the images (960)
    - Input scale: 1/255.0
    - Mean subtraction: None

### Output

Category labels (car) and bounding-box coordinates for each detected vehicle in the input image.

### Examples:

Image must contain a vehicle that is larger than 20x20 pixels after scaling to input size.

![test image](database/trafficcamnet/example_image.jpg)
