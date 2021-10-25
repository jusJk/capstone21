# LPRNet Model

## Overview

The model described in this card is License Plate Recognition Network, which aims to recognize characters in license plates from cropped RGB license plate images. This model is based on models pretrained by NVIDIA with an NVIDIA-owned US license plate dataset and a Chinese license plate dataset.

Transfer learning was performed on NVIDIA's US model to tune it for the EU using the AUTO.RIA Numberplate Dataset (licensed under a
Creative Commons Attribution 4.0 International License), with good performance.

## Model Architecture

This model is a sequence classification model with a ResNet backbone. And it will take the image as network input and produce sequence output.
Training Algorithm

The training algorithm optimizes the network to minimize the connectionist temporal classification (CTC) loss between a ground truth characters sequence of a license plate and a predicted characters sequence. Then the license plate will be decoded from the sequence output of the model through best path decoding method (greedy decoding).

## Reference

    Graves, Alex, et al. "Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks."
    In: Proceedings of the 23rd international conference on Machine learning (2006)
    He, K., Zhang, X., Ren, S., Sun, J.: Deep Residual Learning for Image Recognition. In: CVPR (2015)

## Usage

Primary use case intended for this model is to recognize the license plate from the cropped RGB license plate image.

#### Input Parameters

RGB Images of 3 X 48 X 96 (C H W)

#### Output

Characters id sequence. (DeepStream post-process plugin is needed to get the final license plate)

## Example

The input must be a cropped license plate image like the following:

![image](models/lprnet/database/ca286.png)
![image](models/lprnet/database/cal_plate.jpg)
![image](models/lprnet/database/wy963.png)


## Benchmarks
For LPR Net, we define an accurately recognised license plate as one where the model has managed to read every single letter in the license plate correctly. Reported accuracy will just be the number of license plates correctly read against the total number in the test set.

### US Model

Performance of original US trained NVIDIA Model on various datasets:

<table style="border-collapse:collapse;border-spacing:0" class="tg"><thead><tr><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Dataset<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Model<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Perfect Match (Nvidia TLT)<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Per Character Match<br></th></tr></thead><tbody><tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">East European</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal"> US</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">43.19</span>%</td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">83.81%</span></td></tr><tr><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">OpenALPR</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">US</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">86.48%</span></td><td style="background-color:#FFF;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">97.83%</span></td></tr></tbody></table>

### EU model
ST Engineering's Transfer Learnt EU Model vs Original NVIDIA US Model benchmarked using the above algorithm:

<table style="border-collapse:collapse;border-spacing:0" class="tg"><thead><tr><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Dataset<br></th><th style="background-color:#F4F5F7;border-color:inherit;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Model<br></th><th style="background-color:#F4F5F7;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Perfect Match (Nvidia TLT)<br></th><th style="background-color:#F4F5F7;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">Per Character Match<br></th></tr></thead><tbody><tr><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">East European</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal"> US</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">43.19</span>%</td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">83.81%</span></td></tr><tr><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">East European</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">EU</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">97.00%</span></td><td style="background-color:#FFF;border-color:black;border-style:solid;border-width:1px;color:#172B4D;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal"><span style="font-weight:normal">99.4%</span></td></tr></tbody></table>
