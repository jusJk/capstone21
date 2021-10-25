# Explainability - LPR Net

License plate recognition aims to recognise characters in license plates. It utilises a sequence classification model with a ResNet backbone.

### Sequence classification

The first step in LPR Net is a general sequence classification model. The sequence classification model is described as Connectionist Temporal Classification in:

    Graves, Alex, et al. "Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks."
    In: Proceedings of the 23rd international conference on Machine learning (2006)

The sequence classification model is a general method for temporal classification with Recurrent Neural Networks (RNN) that obviates the need for pre-segmented data, and allows the network to be trained directly for sequence labelling.

This method does not require any license-plate recognition task-specific knowledge, and outperforms many other methods like Hidden-Markov-Model RNNs.

### Decoding the Sequence

We send the horizontal license plates to the Triton server to conduct general sequence classification using a pre-trained license plate recognizer.

After obtaining the sequence output from the license plate, the LPRNet makes use of best path decoding method in order to decode the sequence output of the model into the final predicted characters. Each predicted character is then translated to alphanumeric values using a value-map.

These values are then used to build the output for the final license plate characters.
