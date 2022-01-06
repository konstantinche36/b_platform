from PyQt5 import QtWidgets, QtGui, QtCore

class ImageViewer(QtWidgets.QGraphicsView):
    factor = 2.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setBackgroundRole(QtGui.QPalette.Dark)

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)

    def load_image(self, fileName):
        pixmap = QtGui.QPixmap(fileName)
        if pixmap.isNull():
            return False
        self._pixmap_item.setPixmap(pixmap)
        return True

    def zoomIn(self):
        self.zoom(self.factor)

    def zoomOut(self):
        self.zoom(1 / self.factor)

    def zoom(self, f):
        self.scale(f, f)

    def resetZoom(self):
        self.resetTransform()

    def fitToWindow(self):
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)