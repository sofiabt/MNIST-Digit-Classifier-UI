# MNIST Digit Classifier UI

## Table of Contents

- [About](#about)
- [Architecture](#Architecture)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This project implements a graphical user interface for classifying handwritten digits using a pretrained convolutional `neural network` model trained on the `MNIST` dataset.

# Architecture

The UI is built using `PyQt5` and is structured as follows:

<b>main.py</b> - Launches the PyQt app and contains the main event loop<br>
<b>ui.py</b> - Contains the UI component classes and build logic<br>
<b>models.py</b> - Defines the Keras sequential models for classification <br>
<b>utils.py</b> - Provides utility functions for preprocessing and formatting data

### The main ui components include:
    ImageLabel - A custom QWidget that handles conversion between QImage/QPixmap and Numpy arrays
    DigitLabel - Subclass of ImageLabel that enables drawing digits with mouse events
    build() - Constructs the UI components and layouts using PyQt5 widgets
    classify() - Preprocesses user input, runs inference, and displays results

### Technical detail:
The DigitLabel widget uses a `QPainter` on the underlying `QPixmap` to enable drawing with the mouse
Input images are preprocessed using scaling, centering, and normalization functions in `utils.py`
The preprocessed Numpy array is formatted and passed to the `Keras` model for inference.
The output classification probabilities are displayed using custom QLabel widgets

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

The core dependencies for this project are specified in requirements.txt:

    PyQt5==5.15.4
    tensorflow==2.3.0
    keras==2.4.3 
    numpy==1.19.2
    matplotlib==3.2.2


### Installing

The project doesn't require any installation, execpt for the requirements make sure to have them installed in venv. Activate the env and get ready to use your terminal.<br>


To start, you need to insatll the required libraries.
```
python -m venv .venv
```
```
source .venv/bin/activate
```

Then install the requirements

```
pip install -r requirements.txt
```


## Usage <a name = "usage"></a>
### Command Line Usage

The application accepts the following command line arguments:<br>
```
# Train a model 
python main.py --mode train --model convnet --epochs 10 --out model.h5

# Test a model
python main.py --mode test --model model.h5  

# Launch the UI 
python main.py --mode use
```

### The key arguments are:
    --mode - Either train, test, or use
    --model - Name of model architecture if training, or path to model file
    --epochs - Number of training epochs
    --out - Output path for trained model


To train a model, use `--mode train` and specify a model architecture along with training hyperparameters like `--epochs`.

To test a trained model, use `--mode test` and provide the path to the saved model file.

To launch the UI, `use --mode use`.

See `arguments.py` for the full list of available arguments.