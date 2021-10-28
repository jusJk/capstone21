## Under the Hood

Under the hood, there are 2 major steps to License Plate Recognition. The first is _Detection_, and the second is _Recognition_.

Given this original base image:

![placeholder1](%placeholder1%)

### Preprocessing

As with all image processing problems, the first step is to process the image.
Preprocessing includes a few key steps:

    1. The image is resized into (3, 480, 640)
    2. Mean subtraction and normalization is then performed on the image

The final processed image is then sent to the triton server for inference

### Detection

After being sent to the triton server for inference, we perform detection to detect the bounding boxes of license plates in the image using Nvidia's LPDNet which is based on NVIDIA's DetectNet_v2 detector with ResNet18 as the feature extractor.

This LPDNet inference returns raw output tensors before final post processing is done containing the following steps:

    1. Denormalize the output bbox coordinates which converts bbox from relative coordinates to absolute coordinates.
    2. Threshold the coverage output to get the valid indices for the bboxes based on a pre set coverage threshold.
    3. Cluster the filterred valid boxes using DBSCAN.
    4. Convert filtered boxes into KittiBbox output format with the final absolute coordinates of bbox and confidence scores
    5. Final post processing occurs to return the bbox coordinates and confidence scores for each input image

After postprocessing occurs, we return a bounding box with confidence scores as output.

%placeholder5%

The Bbox coordinates are then used to draw the final detected licence plates.

![placeholder2](%placeholder2%)

These detections are key in the overall goal of license plate recognition (LPR) because LPR performs best when there is little noise in the form of external features other than the license plate.

#### Explaining the prediction

To understand this bounding box detection process a bit more, we can send multiple versions of the picture into the model and observe the variance in confidence.

That is:

    1. We divide the picture into n superpixels using the SLIC algorithm, which groups pixels into similar chunks.
    2. We omit one superpixel every time we hit the model
    3. Regress the change in confidence against omitted superpixel.

This procedure allows us to construct the attention map below.

![placeholder4](%placeholder4%)

In the plot above, red chunks are boxes whose exclusion reduces confidence score, while blue chunks are boxes whose exclusion increases the confidence score. The more intense the color, the stronger the effect.

We use the bounding box to crop into the the license plate, which is then sent to the last phase for license plate recognition

![placeholder3](%placeholder3%)

### Recognition

License plate recognition aims to recognise characters in license plates. It utilises a sequence classification model with a ResNet backbone.

After obtaining the sequence output from the license plate, the LPRNet makes use of _best path decoding method_ in order to decode the sequence output of the model into the final predicted characters.

These characters are then output as the final license plate character.

%placeholder6%
