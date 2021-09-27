# Information on LPD Net

The models described in this card detect one or more license plate objects from a car image and return a box around each object, as well as an lpd label for each object.

Two kinds of pretrained LPD models are delivered --- one is trained on a NVIDIA-owned US license plate dataset and another is trained on a public Chinese City Parking dataset(CCPD).

## Example

![test image](plate.jpg)

## Model Architecture

These models are based on NVIDIA DetectNet_v2 detector with ResNet18 as feature extractor. This architecture, also known as GridBox object detection, uses bounding-box regression on a uniform grid on the input image. Gridbox system divides an input image into a grid which predicts four normalized bounding-box parameters (xc, yc, w, h) and confidence value per output class.

The raw normalized bounding-box and confidence detections needs to be post-processed by a clustering algorithm such as DBSCAN or NMS to produce final bounding-box coordinates and category labels.

## Training algorithm

The training algorithm optimizes the network to minimize the localization and confidence loss for the objects. The training is carried out in two phases. In the first phase, the network is trained with regularization to facilitate pruning.

Following the first phase, we prune the network removing channels whose kernel norms are below the pruning threshold. In the second phase the pruned network is retrained. Regularization is not included during the second phase.
