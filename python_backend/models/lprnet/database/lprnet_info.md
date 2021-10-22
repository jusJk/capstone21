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

## Performance

For LPR Net, we define an accurately recognised license plate as one where the model has managed to read every single letter in the license plate correctly. Reported accuracy will just be the number of license plates correctly read against the total number in the test set.

### Benchmark

Against the EU AUTO.RIA dataset,

LPR EU Model:
Accuracy: 4846 / 4960 or 0.9770161290322581

### Considerations

Model accuracy is affected by the following factors:
