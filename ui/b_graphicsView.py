import sys
from base_objs.nb_platform import BPlatform
from b_mat.b_mat_worker import generate_mat_from_image
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QImage, QWheelEvent
from PyQt5.QtGui import QPixmap
from base_objs.b_obj import BWindowWorker
from PyQt5.QtCore import Qt


class M1_QGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, b_platform: BPlatform, parent):
        super(M1_QGraphicsView, self).__init__()
        self.setMouseTracking(True)

        self.b_platform: BPlatform = b_platform
        self.parent = parent
        self.result_f_mat = b_platform.result_f_mat
        self.is_press_rb = False

        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.item)

        self.action_list = []
        self.action_list_size = 10
        self.reset_mode_action_list()

        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def create_mode_enable(self):
        self.reset_mode_action_list()
        self.action_list[0] = True

    def select_mode_enable(self):
        self.reset_mode_action_list()
        self.action_list[1] = True

    def move_mode_enable(self):
        self.reset_mode_action_list()
        self.action_list[2] = True

    def reset_mode_action_list(self):
        self.action_list = [False] * 10

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Left:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - 10)
        elif event.key() == Qt.Key_Right:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + 10)
        elif event.key() == Qt.Key_Up:
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - 10)
        elif event.key() == Qt.Key_Down:
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + 10)
        elif event.key() == Qt.Key_C:
            self.create_mode_enable()
        elif event.key() == Qt.Key_S:
            self.select_mode_enable()
        elif event.key() == Qt.Key_M:
            self.move_mode_enable()
        elif event.key() == Qt.Key_Escape:
            self.reset_mode_action_list()
            self.b_platform.selected_point = None
            self.b_platform.selected_figure = None
            self.reload_mat_and_update()
        elif event.key() == Qt.Key_Backspace:
            if self.action_list[0]:
                self.b_platform.delete_point_last_point()
        elif event.key() == Qt.Key_Delete:
            print('DELETE')
            print('Objects ::: ', self.action_list[2], self.b_platform.selected_figure, self.b_platform.last_selected_point)
            if self.action_list[2] and self.b_platform.selected_figure and self.b_platform.last_selected_point:
                # self.b_platform.delete_point(self.b_platform.last_selected_point)
                # self.b_platform.delete_point(self.b_platform.selected_point)
                self.b_platform.delete_point_from_figure(self.b_platform.last_selected_point)
                print('Is deleted')
        self.reload_mat_and_update()

    def wheelEvent(self, event: QWheelEvent):
        factor = 1.1
        if event.angleDelta().x() or event.angleDelta().y() < 0:
            factor = 0.9
            self.b_platform.set_line_width(self.b_platform.line_width + 0.02)
            self.b_platform.dot_radius += 0.03
        else:
            self.b_platform.set_line_width(self.b_platform.line_width - 0.02)
            self.b_platform.dot_radius -= 0.03
        view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        self.centerOn(scene_pos)
        self.scale(factor, factor)
        delta = self.mapToScene(view_pos) - self.mapToScene(
            self.viewport().rect().center())
        self.centerOn(scene_pos - delta)
        self.reload_mat_and_update()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        x, y = self.get_coors(a0)
        if self.action_list[0]:
            self.b_platform.draw_temp_line(x, y)
            self.update_mat(self.b_platform.result_f_mat)
        elif self.action_list[2]:
            if self.is_press_rb:
                self.b_platform.do_action(x, y, self.action_list)
                self.reload_mat_and_update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.is_press_rb = False
        self.b_platform.last_selected_point = self.b_platform.selected_point
        self.b_platform.selected_point = None

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.store_last_x_y_co_position(event)
        x, y = self.get_coors(event)
        self.b_platform.do_action(x, y, self.action_list)
        if event.button() == Qt.LeftButton and self.action_list[2] and self.b_platform.co_pop_to_point(x, y):
            print(111111111)
            self.is_press_rb = True
        self.reload_mat_and_update()

    def update_mat(self, mat):
        height, width, channel = self.b_platform.result_f_mat.shape
        bytesPerLine = 4 * width
        self.pixmap = QPixmap(
            QImage(self.b_platform.result_f_mat.data, width, height, bytesPerLine, QImage.Format_RGBA8888).rgbSwapped())
        self.item.setPixmap(self.pixmap)

    def get_coors(self, event):
        view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        return scene_pos.x(), scene_pos.y()

    def reload_mat_and_update(self):
        self.b_platform.redraw_mat()
        self.update_mat(self.b_platform.result_f_mat)

    def store_last_x_y_co_position(self, event):
        self.last_mouse_x = event.x()
        self.last_mouse_y = event.y()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m1 = M1_QGraphicsView(BPlatform(generate_mat_from_image('./pic1.jpg')), None)
    m1.update_mat(m1.b_platform.result_f_mat)
    m1.show()
    BWindowWorker.IS_NEW_CREATE_MODE = True
    sys.exit(app.exec_())
