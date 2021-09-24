# Information on LPD Net

This model card is a pipeline of 2 models, described below.

## LPD Net Model

The first model is License Plate Detection Net, based on DetectNet. This model detects a license plate in an image and crops into it. See the documentation for more information.

## LPR Net Model

The second model is License Plate Recognition Net. This model takes a cropped image of a license plate and reads it, producing confidence scores in the process. See the documentation for more information.

## LPD + LPR Net Model

The LPD+LPR Net Model simply consists of the LPD and LPRNet models working together in a pipeline. The pipeline handles all the data processing steps and intermediate data flows to provide end to end inference.
