"""
deepnet1, deepnet2 and convnet define Keras sequential models for image classification.

deepnet1 is a simple model with a flatten layer and a dense output layer.

deepnet2 adds a hidden relu layer before the output. 

convnet uses convolutional and pooling layers before the dense output.
"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Reshape, Dense, Activation, Conv2D, MaxPooling2D, Dropout

import utils

def deepnet1():
    model = Sequential()

    model.add(Flatten(input_shape=utils.IMG_SHAPE))

    model.add(Dense(utils.NUM_CLASSES))
    model.add(Activation("softmax"))

    return model

def deepnet2():
    model = Sequential()

    model.add(Flatten(input_shape=utils.IMG_SHAPE))

    model.add(Dense(128))
    model.add(Activation("relu"))

    model.add(Dense(utils.NUM_CLASSES))
    model.add(Activation("softmax"))

    return model

def convnet():
    model = Sequential()

    model.add(Reshape((*utils.IMG_SHAPE, 1), input_shape=utils.IMG_SHAPE))

    model.add(Conv2D(32, kernel_size=(3, 3)))
    model.add(Activation("relu"))

    model.add(Conv2D(64, kernel_size=(3, 3)))
    model.add(Activation("relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    model.add(Dense(128))
    model.add(Activation("relu"))

    model.add(Dense(utils.NUM_CLASSES))
    model.add(Activation("softmax"))

    return model