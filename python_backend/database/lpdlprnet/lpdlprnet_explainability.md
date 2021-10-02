## Under the Hood

Under the hood, there are 2 major steps to License Plate Recognition. The first is _Detection_, and the second is _Recognition_.

Given this original base image:

![placeholder1](%placeholder1%)

### Preprocessing

As with all image processing problems, the first step is to process the image.

### Detection

The next step is the detection phase, where we use LPD Net to detect license plates. This is done using DetectNet - a standard library that is used industry wide for object detection problems. After using LPDNet to detect the license plate, we crop into the detected license plate. The reason we do this is because LPR Net performs best when there is less noise in the image.

The output of LPDNet is a bounding box which we use to crop into the detected license plate.

![placeholder2](%placeholder2%)

### Recognition

Lastly, we reach the recognition phase. LPR Net runs on the output from LPD Net to product a license plate.

### Results

We summarise the results in the following table:

%placeholder3%
