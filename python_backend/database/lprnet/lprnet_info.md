# Information on LPR Net

The model described in this card is license plate recognition network, which aims to recognize characters in license plates from cropped RGB license plate images. Two pretrained LPRNet models are delivered --- one is trained on a NVIDIA-owned US license plate dataset and another is trained on a Chinese license plate dataset.

## Usage

Primary use case intended for this model is to recognize the license plate from the cropped RGB license plate image.

#### Input Parameters

RGB Images of 3 X 48 X 96 (C H W)

#### Output

Characters id sequence. (DeepStream post-process plugin is needed to get the final license plate)

## Example

The input must be a cropped license plate image as follows:
![image](ca286.png)
