## Under the Hood

Under the hood, there are 2 major steps to License Plate Recognition. The first is _Detection_, and the second is _Recognition_.

Given this original base image:

![placeholder1](%placeholder1%)

### Preprocessing

For this image processing problem, the first step is to process the image.

### Detection

The next step is the detection phase, where we use LPD Net to detect license plates. This is done using DetectNet - a standard library that is used industry wide for object detection problems.

The output of LPDNet is as follows:

%placeholder5%

This represents a bounding box which we use to outline the detected license plate drawn below.

![placeholder2](%placeholder2%)

After drawing the bounding box, we crop into the detected license plate and feed that as input into the recognition stage - which performs better when there are less "distractions" in the image.

![placeholder3](%placeholder3%)

### Recognition

Lastly, we reach the recognition phase. LPR Net runs on the output from LPD Net to product a license plate. This returns the following output:

%placeholder6%
