# Information on LPD Net

This model card is a pipeline of 2 models, described below.

## LPD Net

### Model Overview

The model described in this card detect one or more license plate objects from a car image and return a box around each object, as well as an lpd label for each object. This model is based on NVIDIA's pretrained models, which are trained on a NVIDIA-owned US license plate dataset and a public Chinese City Parking dataset(CCPD).

### Model Architecture

These models are based on **NVIDIA DetectNet_v2** detector with **ResNet18** as feature extractor. This architecture, also known as **GridBox object detection**, uses bounding-box regression on a uniform grid on the input image. Gridbox system divides an input image into a grid which predicts four normalized bounding-box parameters (xc, yc, w, h) and confidence value per output class.

The raw normalized bounding-box and confidence detections needs to be post-processed by a clustering algorithm such as **DBSCAN** or **NMS** to produce final bounding-box coordinates and category labels. This is done by the image clients that the model catalog provides.

### Training Algorithm

The training algorithm optimizes the network to minimize the localization and confidence loss for the objects. The training is carried out in two phases. In the first phase, the network is trained with regularization to facilitate pruning. Following the first phase, we prune the network removing channels whose kernel norms are below the pruning threshold. In the second phase the pruned network is retrained. Regularization is not included during the second phase.

### Citations

    Redmon, J., Divvala, S., Girshick, R., Farhadi, A.: You only look once: Unified, real-time object detection. In: CVPR. (2016)
    Erhan, D., Szegedy, C., Toshev, A., Anguelov, D.: Scalable object detection using deep neural networks, In: CVPR. (2014)
    He, K., Zhang, X., Ren, S., Sun, J.: Deep Residual Learning for Image Recognition. In: CVPR (2015)

### Usage

Primary use case intended for these models is detecting license plates in a color (RGB) image. The model can be used to detect license plates from photos and videos by using appropriate video or image decoding and pre-processing.

#### Input

For EU license plate

    - Color Images of resolution 640 X 480 X 3 (W x H x C)
    - Channel Ordering of the Input: NCHW, where
        - N = Batch Size,
        - C = number of channels (3),
        - H = Height of images (480),
        - W = Width of the images (640)
    - Input scale: 1/255.0
    - Mean subtraction: None

#### Output

Category labels (lpd) and bounding-box coordinates for each detected license plate in the input image.

#### Examples:

Image must contain a vehicle with a visible number plate.

![test image](models/lpdnet/database/overlay_lpdnet_plate.jpg)

## LPRNet Model

### Overview

The model described in this card is License Plate Recognition Network, which aims to recognize characters in license plates from cropped RGB license plate images. This model is based on models pretrained by NVIDIA with an NVIDIA-owned US license plate dataset and a Chinese license plate dataset.

Transfer learning was performed on NVIDIA's US model to tune it for the EU using the AUTO.RIA Numberplate Dataset (licensed under a
Creative Commons Attribution 4.0 International License), with good performance.

### Model Architecture

This model is a sequence classification model with a ResNet backbone. And it will take the image as network input and produce sequence output.
Training Algorithm

The training algorithm optimizes the network to minimize the connectionist temporal classification (CTC) loss between a ground truth characters sequence of a license plate and a predicted characters sequence. Then the license plate will be decoded from the sequence output of the model through best path decoding method (greedy decoding).

### Reference

    Graves, Alex, et al. "Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks."
    In: Proceedings of the 23rd international conference on Machine learning (2006)
    He, K., Zhang, X., Ren, S., Sun, J.: Deep Residual Learning for Image Recognition. In: CVPR (2015)

### Usage

Primary use case intended for this model is to recognize the license plate from the cropped RGB license plate image.

#### Input Parameters

RGB Images of 3 X 48 X 96 (C H W)

#### Output

Characters id sequence. (DeepStream post-process plugin is needed to get the final license plate)

### Example

The input must be a cropped license plate image like the following:

![image](models/lprnet/database/ca286.png)
![image](models/lprnet/database/cal_plate.jpg)
![image](models/lprnet/database/wy963.png)


## LPD + LPR Net Model

The LPD+LPR Net Model simply consists of the LPD and LPRNet models working together in a pipeline. The pipeline handles all the data processing steps and intermediate data flows to provide end to end inference.
