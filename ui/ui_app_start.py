from PyQt5 import QtWidgets, QtGui, QtCore
from ui.des import *
from ui.des_m2 import *
import sys


class ImageViewer():
    factor = 2.0

    def __init__(self, main_window):
        self.q_graphics_view = main_window.get_self_ui().graphicsView
        # print(q_graphics_view.parentWidget().height(), q_graphics_view.parentWidget().width())
        # self.q_graphics_view.setGeometry(QtCore.QRect(0, 0, main_window.width(), main_window.height()))
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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.view = ImageViewer(self)
        self.ui.actionOpen_file.triggered.connect(self.open)
        self.ui.actionZoom_in.triggered.connect(self.view.zoomIn)
        self.ui.actionZoom_out.triggered.connect(self.view.zoomOut)
        self.ui.actionNormal_view.triggered.connect(self.view.resetZoom)
        self.modal = ModalM2(self)
        self.modal.show()

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
        if fileName:
            is_loaded = self.view.load_image(fileName)
            # self.fitToWindowAct.setEnabled(is_loaded)
            # self.updateActions()
            # todo


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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = BaseWin()
    myapp.show()
    sys.exit(app.exec_())
