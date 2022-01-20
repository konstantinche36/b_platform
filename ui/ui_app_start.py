# from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5.QtGui import QWheelEvent
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtCore import Qt, QEvent
from PIL import Image

from base_objs.b_obj import BWindowWorker, BAreaWorker, BFigureWorker, BArea, BLayer
from b_mat.b_mat_worker import generate_mat_from_image
from base_objs.nb_platform import BPlatform
from PyQt5.QtGui import QFont, QPixmap, QMouseEvent, QImage, QWheelEvent

from ui.des import *
from ui.des_m2 import *
from ui.des_m3 import *
import sys


class ImageViewer():
    factor = 2.0

    def __init__(self, main_window):
        self.q_graphics_view = main_window.get_self_ui().graphicsView
        self.q_graphics_view.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
        )
        self.q_graphics_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.q_graphics_view.setBackgroundRole(QtGui.QPalette.Dark)

        scene = QtWidgets.QGraphicsScene()
        self.q_graphics_view.setScene(scene)

        self.q_graphics_view._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.q_graphics_view._pixmap_item)

    def load_image(self, fileName):
        pixmap = QtGui.QPixmap(fileName)
        if pixmap.isNull():
            return False
        self.q_graphics_view._pixmap_item.setPixmap(pixmap)
        return True

    def zoomIn(self):
        self.zoom(self.factor)

    def zoomOut(self):
        self.zoom(1 / self.factor)

    def zoom(self, f):
        self.q_graphics_view.scale(f, f)

    def resetZoom(self):
        self.q_graphics_view.resetTransform()

    def fitToWindow(self):
        self.q_graphics_view.fitInView(self.q_graphics_view.sceneRect(), QtCore.Qt.KeepAspectRatio)


class BaseWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_loaded = None
        self.b_platform = None
        self.mat = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.view = ImageViewer(self)
        self.ui.actionOpen_file.triggered.connect(self.open)
        self.ui.actionZoom_in.triggered.connect(self.view.zoomIn)
        self.ui.actionZoom_out.triggered.connect(self.view.zoomOut)
        self.ui.actionNormal_view.triggered.connect(self.view.resetZoom)


    def get_self_ui(self):
        return self.ui

    def open(self):
        image_formats = " ".join(
            ["*." + image_format.data().decode() for image_format in QtGui.QImageReader.supportedImageFormats()]
        )
        print('open!!!')

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open Image"),
            QtCore.QDir.currentPath(),
            self.tr("Image Files({})".format(image_formats)),
        )
        self.show_statusbar_msm('Open file: ' + fileName)
        if fileName:
            if fileName.endswith('.jpg'):
                im1 = Image.open(fileName)
                fileName = fileName[0:-3] + 'png'
                print(fileName)
                im1.save(fileName)
            self.mat = generate_mat_from_image(fileName)
            # print('self.mat.shape' + str(self.mat.shape))
            self.is_loaded = self.view.load_image(fileName)
            self.start_modal_windows()
            self.b_platform = BPlatform(self.mat)
            print('FINISH')
            # todo

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.is_loaded:
            if a0.key() == Qt.Key_Escape:
                print('Escape button')
                self.modal3.reset_all_button_color()

    def start_modal_windows(self):
        if self.is_loaded:
            self.modal = ModalM2(self)
            self.modal.show()
            self.modal3 = ModalM3(self)
            self.modal3.show()

    def show_statusbar_msm(self, msm, sec=6000):
        self.ui.statusbar.showMessage(msm, sec)

    def update(self) -> None:
        height, width, channel = self.result_f_mat.shape
        bytesPerLine = 4 * width
        qImg = QImage(self.result_f_mat.data, width, height, bytesPerLine, QImage.Format_RGBA8888).rgbSwapped()
        pixmap = QPixmap(qImg)
        pixmap_scaled = pixmap.scaled(900, 1200)
        self.img.setPixmap(pixmap_scaled)
        self.img.move(5, 5)


class ModalM2(QtWidgets.QWidget):
    def __init__(self, parent=BaseWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.parent = parent
        self.modal = Ui_Form()
        self.modal.setupUi(self)
        self.def_start_val()

        self.modal.pushButton.clicked.connect(self.set_factor)

    def def_start_val(self):
        self.parent.get_self_ui()
        self.modal.lineEdit.setText(str(self.parent.view.factor))

    def set_factor(self):
        self.parent.view.factor = float(self.modal.lineEdit.text())
        self.modal.lineEdit.setText(str(self.parent.view.factor))
        self.def_start_val()


class ModalM3(QtWidgets.QWidget):
    def __init__(self, parent=BaseWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.base_window = parent
        self.modal = Ui_Form3()
        self.modal.setupUi(self)
        self.pressed_button_background_style = 'background-color: rgb(255, 255, 128);'
        self.unpressed_button_background_style = 'background-color: rgb(240, 240, 240);'
        self.pressed = None

        self.modal.pushButton.clicked.connect(self.pressed_butt_create_figure)
        self.modal.pushButton_3.clicked.connect(self.pressed_butt_foo)

    def pressed_butt_create_figure(self):
        self.modal.pushButton.setStyleSheet(self.pressed_button_background_style)
        self.pressed = True
        self.base_window.show_statusbar_msm('Pressed button: "create figure"', sec=0)

    def pressed_butt_foo(self):
        if self.pressed:
            print('self.pressed')
            self.reset_all_button_color()

    def reset_all_button_color(self):
        if self.pressed:
            for button in self.modal.gridLayoutWidget.findChildren(QtWidgets.QPushButton):
                button.setStyleSheet(self.unpressed_button_background_style)
            self.pressed = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = BaseWin()
    myapp.show()
    sys.exit(app.exec_())
