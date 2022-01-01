import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QScrollArea
from PyQt5.QtGui import QFont, QPixmap, QMouseEvent, QImage
from PyQt5 import QtCore, QtGui, QtWidgets


class BPBaseWindow(QWidget):
    def __init__(self, mat):
        super().__init__()
        self.mat = mat
        self.curr_key = ''
        self.initialize()


    def initialize(self):
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800,600)
        # self.displayImages()
        self.displayMatImages()
        self.setWindowTitle('BPlatform')
        self.show()

    def displayMatImages(self):
        self.img = QLabel(self)
        print(self.mat)
        height, width, channel = self.mat.shape
        bytesPerLine = 4 * width
        qImg = QImage(self.mat.data, width, height, bytesPerLine, QImage.Format_RGBA8888).rgbSwapped()
        pixmap = QPixmap(qImg)
        pixmap_scaled = pixmap.scaled(900, 1200)
        self.img.setPixmap(pixmap_scaled)
        self.img.move(5, 5)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, 800, 600)
        self.scroll_area.setWidget(self.img)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.left_button_press()
        elif event.button() == Qt.RightButton:
            self.right_button_press()
        elif event.button() == Qt.MiddleButton:
            self.middle_button_press()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            print('Space button')
            self.curr_key =  '111'
        elif event.key() == Qt.Key_Escape:
            print('Escape button')
            self.curr_key = '222'


    def get_key(self):
        return self.curr_key

    def left_button_press(self):
        print('Left button')

    def right_button_press(self):
        print('Right button')

    def middle_button_press(self):
        print('Middle button')


    def displayImages(self):
        path_to_image = 'resize_test_img.png'
        try:
            with open(path_to_image):
                self.img = QLabel(self)
                pixmap = QPixmap(path_to_image)
                pixmap_scaled = pixmap.scaled(900, 1200)
                self.img.setPixmap(pixmap_scaled)
                self.img.move(5, 5)
            print('Trying to show a picture')
        except FileNotFoundError:
            print('Image not found!')


# def ui_show_window():
#     print('Start UI')
#     app = QApplication(sys.argv)
#     window = BPBaseWindow()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    print('Start')
    app = QApplication([])
    window = BPBaseWindow(None)
    sys.exit(app.exec_())
    print('end')
