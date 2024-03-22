import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, qRed, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog
import numpy

import utils


"""
ImageLabel class that inherits from QLabel and allows converting between 
QImage/QPixmap and numpy array for display and pixel manipulation.

The image() method converts the underlying QPixmap to a numpy array for 
manipulation. 

The setImage() method converts a numpy array back to a QPixmap for display.
"""
class ImageLabel(QLabel):
    def image(self):
        qImage = self.pixmap().toImage()

        img = numpy.zeros((qImage.height(), qImage.width()), dtype="int32")

        for j in range(qImage.height()):
            for i in range(qImage.width()):
                gray = qRed(qImage.pixel(i, j))
                img[j][i] = gray

        return img

    def setImage(self, img):
        qImage = QImage(img.shape[1], img.shape[0], QImage.Format_RGB888)

        for j in range(qImage.height()):
            for i in range(qImage.width()):
                gray = img[j][i]
                qImage.setPixelColor(i, j, QColor(gray, gray, gray))

        qPixmap = QPixmap(qImage)
        self.setPixmap(qPixmap)


"""DigitLabel class that inherits from ImageLabel to allow drawing digits by dragging mouse.

Overrides mouse event handlers to draw lines following mouse drag, 
using an internal QPainter on the underlying QPixmap.

Provides resetImage() method to clear the image.
"""
class DigitLabel(ImageLabel):
    def __init__(self):
        super().__init__()

        self.x_old = None
        self.y_old = None

        self.factor = 10

        self.size = 200
        self.qPenSize = 10

        self.resetImage()

    def resetImage(self):
        image = numpy.zeros((self.size, self.size), dtype="int32")
        self.setImage(image)

    def mousePressEvent(self, event):
        self.x_old = event.x()
        self.y_old = event.y()

    def mouseMoveEvent(self, event):
        qPen = QPen(QColor(255, 255, 255), self.qPenSize, Qt.SolidLine)

        qPainter = QPainter()
        qPainter.begin(self.pixmap())
        qPainter.setPen(qPen)
        qPainter.drawLine(self.x_old, self.y_old, event.x(), event.y())
        qPainter.end()

        self.update()

        self.x_old = event.x()
        self.y_old = event.y()


"""
Builds the MNIST digit classifier UI.

Creates the UI widgets like the digit label for drawing, preprocess views, 
classify views, etc. Connects signals to slots like classifying on mouse 
release. Loads model and provides classify and reset functions.
"""
def build(model):
    def classify(event=None):
        nonlocal digit_label, prepro_digit_labels, classif_labels, model

        img = digit_label.image()
        imgs = utils.preprocess(img)

        for i, img in enumerate(imgs):
            prepro_digit_labels[i].setImage(img)

        x = utils.format_x([imgs[-1]])
        y = model.predict(x)

        distr = y[0]
        claz = numpy.argmax(distr)

        for i, (class_label, proba_label) in enumerate(classif_labels):
            if i == claz:
                class_label.setStyleSheet("background-color: grey; padding: 2px 3px")
                proba_label.setStyleSheet("background-color: pink; padding: 2px 3px")
            else:
                class_label.setStyleSheet("background-color: white; padding: 2px 3px")
                proba_label.setStyleSheet("background-color: white; padding: 2px 3px")

            percentage = round(distr[i] * 100, 1)
            proba_label.setText(str(percentage) + "%")

    def reset():
        nonlocal digit_label
        digit_label.resetImage()


    def importer():
        reset()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "open a file", "",
                                                   "All Files (*);;Python Files (*.py)", options=options)
        px = QPixmap(file_path)
        digit_label.setPixmap(px)
        data = digit_label.image()
        try:
            digit_label.setImage(img=data)
            classify()
        except:
            import traceback
            traceback.print_exc()

    app = QApplication(sys.argv)

    digit_grid = QGridLayout()

    digit_label = DigitLabel()
    digit_label.mouseReleaseEvent = classify
    digit_grid.addWidget(digit_label, 0, 0, utils.NUM_PROCESS_STEPS, 1, Qt.AlignCenter)

    prepro_digit_labels = []

    for i in range(utils.NUM_PROCESS_STEPS):
        row = i

        prepro_digit_label = ImageLabel()
        digit_grid.addWidget(prepro_digit_label, row, 1, Qt.AlignCenter)

        prepro_digit_labels.append(prepro_digit_label)

    import_button = QPushButton("importer une image")
    import_button.clicked.connect(importer)
    import_button.setMaximumWidth(100)
    reset_button = QPushButton("reprendre")
    reset_button.setMaximumWidth(100)
    reset_button.clicked.connect(reset)

    classif_grid = QGridLayout()

    classif_labels = []

    for i in range(utils.NUM_CLASSES):
        class_label = QLabel(str(i))
        class_label.setStyleSheet("padding: 2px 4px")
        classif_grid.addWidget(class_label, i, 0, Qt.AlignCenter)

        proba_label = QLabel()
        classif_grid.addWidget(proba_label, i, 1, Qt.AlignCenter)

        classif_labels.append([class_label, proba_label])

    reset()

    grid = QGridLayout()

    grid.addWidget(import_button, 0, 0)
    grid.addLayout(digit_grid, 1, 0)
    grid.addWidget(reset_button, 2, 0)
    grid.addLayout(classif_grid, 1, 1)
    w = QWidget()
    w.setGeometry(400, 200, 700, 370)
    w.setWindowIcon(QIcon('icon2.png'))
    w.setStyleSheet("background-image: url('4.jpg'); background-attachment: ")

    w.setWindowTitle("Classificateur des Chiffres Manuscrits")
    w.setMinimumSize(QtCore.QSize(700, 370))
    w.setMaximumSize(QtCore.QSize(700, 370))
    w.setLayout(grid)
    w.show()

    sys.exit(app.exec_())



