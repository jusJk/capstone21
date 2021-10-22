# LPD Net

## Model Overview

The model described in this card detect one or more license plate objects from a car image and return a box around each object, as well as an lpd label for each object. This model is based on NVIDIA's pretrained models, which are trained on a NVIDIA-owned US license plate dataset and a public Chinese City Parking dataset (CCPD).

Depending on the user, this model can serve a model trained for EU or US license plates. Results are described below.

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

Primary use case intended for these models is detecting license plates in a color (RGB) image. The model can be used to detect license plates from photos and videos by using appropriate video or image decoding and pre-processing.

### Input

For EU license plate

    - Color Images of resolution 640 X 480 X 3 (W x H x C)
    - Channel Ordering of the Input: NCHW, where
        - N = Batch Size,
        - C = number of channels (3),
        - H = Height of images (480),
        - W = Width of the images (640)
    - Input scale: 1/255.0
    - Mean subtraction: None

### Output

Category labels (lpd) and bounding-box coordinates for each detected license plate in the input image.

### Examples:

Image must contain a vehicle with a visible number plate.

![test image](models/lpdnet/database/overlay_lpdnet_plate.jpg)

## Benchmarks
We use a **strict** benchmarking IOU algorithm as follows:

    1. For each image, form a set of ground truth bounding boxes G.
    2. For each predicted box, check if the IOU with any of the boxes in G > threshold (0.5).
       If yes, it is considered a match and the matched box is removed from set G.
    3. For each dataset, we quantify the performance as the number of matched bounding boxes / total number of bounding boxes.

### US Model
The original NVIDIA US Model benchmarked using the above algorithm:

<table style="border-collapse:collapse;border-spacing:0" class="tg"><thead><tr><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Dataset<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Model<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Number of Matched Boxes<br></th><th style="background-color:#F4F5F7;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Total Bounding Boxes<br></th><th style="background-color:#F4F5F7;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Percentage of Matched Boxes<br></th></tr></thead><tbody><tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">ALPR_US</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">US</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">166</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">222</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">74.8%</span></td></tr></tbody></table>


### EU model
ST Engineering's Transfer Learnt EU Model vs Original NVIDIA US Model benchmarked using the above algorithm:

<table style="border-collapse:collapse;border-spacing:0" class="tg"><thead><tr><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Dataset<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Model<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Number of Matched Boxes<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Total Bounding Boxes<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Percentage of Matched Boxes<br></th></tr></thead><tbody><tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">romania_train</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">US</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">126</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">521</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">24.2%</span></td></tr><tr><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">romania_valid</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">US</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">49</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">131</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">37.4%</span></td></tr><tr><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">romania_train</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">EU</td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">517</td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">521</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">99</span>.2%</td></tr><tr><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">romania_valid</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">EU</td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">126</td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">131</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">96.7%</span></td></tr></tbody></table>


## Performance Considerations

There some factors that cause LPDNet to perform poorly.

### License Plate Image Ratio

LPDNet is sensitive to the following ratios:

    1. Aspect ratio (width of image/height of image)
    2. Width ratio (width of image/width of license plate)
    3. Height ratio (height of image/height of license plate)

In particular, LPDNet performs poorer on extreme width and height ratios.

The picture below shoes the distribution of Width Ratio and Height Ratio for matched License plates (orange) vs unmatched license plates (blue)
![ratio image](models/lpdnet/database/imageratio.png)

The picture below shoes the distribution of image Aspect Ratios for matched License plates (orange) vs unmatched license plates (blue)
![aspect image](models/lpdnet/database/aspect.png)
In general, the sweet spot is where a license plate is around 20% of the width and height picture, and landscape photos perform better than portraits.

### Image Content

LPDNet is also sensitive to image content.

    1. Brightness (average pixel brightness of image when converted to greyscale, ranges from 0-255)
    2. Gates and fences tend to be confused for license plates
    3. Orientation/perspective of license plates
