# Explainability - Traffic Cam Net

### Preprocessing

As with all image processing problems, the first step is to process the image.
Preprocessing includes a few key steps:

    1. The image is resized into (3, 544, 960)
    2. Mean subtraction and normalization is then performed on the image

The final processed image is then sent to the triton server for inference

### Detection

After being sent to the triton server for inference, we perform detection to detect the bounding boxes of the vehicles in the image using Nvidia's TrafficCamNet which is based on NVIDIA's DetectNet_v2 detector with ResNet18 as the feature extractor.

This TrafficCamNet inference returns raw output tensors before final post processing is done containing the following steps:

    1. Denormalize the output bbox coordinates which converts bbox from relative coordinates to absolute coordinates.
    2. Threshold the coverage output to get the valid indices for the bboxes based on a pre set coverage threshold.
    3. Cluster the filterred valid boxes using DBSCAN.
    4. Convert filtered boxes into KittiBbox output format with the final absolute coordinates of bbox and confidence scores
    5. Final post processing occurs to return the bbox coordinates and confidence scores for each input image

After postprocessing occurs, we return a bounding box with confidence scores as output.

The Bbox coordinates are then used to draw the final detected vehicles.

### Demo

