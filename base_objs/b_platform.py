import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsItem
from ui_app_start import BPBaseWindow
from utils import utils
from base_objs.b_obj import BCPoint, BPoint, BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD, \
    BAreaDrawer, \
    BLayerWorker
from numpy import ndarray

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QScrollArea
from PyQt5.QtGui import QFont, QPixmap, QMouseEvent, QImage, QWheelEvent
from PyQt5 import QtCore, QtGui, QtWidgets

figure_name = utils.get_random_name()


class BPlatform(QWidget):
    REDRAW_MENU = False
    reset_line_params = None

    def __init__(self):
        super().__init__()
        self.name = None
        self.windows_worker = None
        self.b_area = None
        self.b_area_worker = None
        self.b_figure_worker = None
        self.result_mat = None
        self.b_area_drawer = None
        self.layer_mat = self.result_mat
        self.temp_mat = None
        self.mark_create_figure_is_true = None
        self.b_layer_worker = None
        self.active_figure: BFigure = None
        self.active_point: BPoint = None
        self.cur_mat = self.result_mat

        self.layer_mat = self.result_mat
        self.active_layer = None
        self.source_f_mat = None
        self.temp_f_mat = None
        self.result_f_mat = None
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.created_f_mat = None
        self.selected_figure = None
        self.select_point: BPoint = None
        self.is_press_rb = None

    def base_obj_init(self,windows_worker: BWindowWorker, base_mat: ndarray, b_area: BArea, b_area_worker: BAreaWorker,
                 b_figure_worker: BFigureWorker, name='Default_platform_name'):
        self.windows_worker = windows_worker
        self.source_f_mat = base_mat
        self.temp_f_mat = base_mat
        self.result_f_mat = base_mat
        self.b_area = b_area
        self.b_area_worker = b_area_worker
        self.b_area_drawer = BAreaDrawer(self.b_area_worker)
        self.b_figure_worker = b_figure_worker
        self.result_mat = self.b_area.get_base_mat()
        self.temp_mat = np.copy(self.result_mat)
        self.name = name
        self.b_layer_worker = BLayerWorker('default_worker', base_mat)
        self.initialize()

    def initialize(self):
        self.setGeometry(100, 100, 800, 600)
        # self.setFixedSize(800,600)
        self.displayMatImages()
        self.setWindowTitle('BPlatform')
        self.show()

    def displayMatImages(self):
        self.img = QLabel(self)
        height, width, channel = self.result_f_mat.shape
        bytesPerLine = 4 * width
        qImg = QImage(self.result_f_mat.data, width, height, bytesPerLine, QImage.Format_RGBA8888).rgbSwapped()
        pixmap = QPixmap(qImg)
        pixmap_scaled = pixmap.scaled(900, 1200)
        self.img.setPixmap(pixmap_scaled)
        self.img.move(5, 5)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, 800, 600)
        self.scroll_area.setWidget(self.img)

        self.info_label = QLabel(self)
        self.info_label.setGeometry(10, 10, 200, 20)
        self.mode_label = QLabel(self)
        self.mode_label.setGeometry(10, 30, 200, 20)
        self.mode_label2 = QLabel(self)
        self.mode_label2.setGeometry(10, 50, 200, 20)

    def update(self) -> None:
        height, width, channel = self.result_f_mat.shape
        bytesPerLine = 4 * width
        qImg = QImage(self.result_f_mat.data, width, height, bytesPerLine, QImage.Format_RGBA8888).rgbSwapped()
        pixmap = QPixmap(qImg)
        pixmap_scaled = pixmap.scaled(900, 1200)
        self.img.setPixmap(pixmap_scaled)
        self.img.move(5, 5)


    def display_info_label(self, text):
        self.info_label.setText(text)

    def display_mode_label(self, text):
        self.mode_label.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_N:
            self.display_info_label('Pressed: n')
            self.display_mode_label('None mode')
            BWindowWorker.IS_NEW_MODE = True
        elif event.key() == Qt.Key_J:
            self.display_info_label('Pressed: j')
            self.display_mode_label('NEW create mode')
            self.esc_reset()
            BWindowWorker.IS_NEW_CREATE_MODE = True
            self.init_new_figure()
        elif event.key() == Qt.Key_S:
            self.display_info_label('Pressed: s')
            self.display_mode_label('Select figure mode')
            BWindowWorker.IS_SELECT_FIGURE_MODE = True
        elif event.key() == Qt.Key_Backspace and BWindowWorker.IS_NEW_CREATE_MODE:
            self.display_info_label('Pressed: backspace')
            self.b_figure_worker.remove_last_figure_point()
            self.reload_mat()
        elif event.key() == Qt.Key_Q:
            sys.exit()
        elif event.key() == Qt.Key_Space:
            print('Space button')
            self.curr_key =  '111'
        elif event.key() == Qt.Key_Escape:
            print('Escape button')
            self.esc_reset()
            # self.init_new_figure()
            # self.result_f_mat = self.temp_f_mat
            self.save_to_result_mat()


    def get_key(self):
        return self.curr_key

    def left_button_press(self):
        print('Left button')

    def right_button_press(self):
        print('Right button')

    def middle_button_press(self):
        print('Middle button')

    def scrolled(scrollbar, value):
        if value == scrollbar.maximum():
            print('reached max')  # that will be the bottom/right end
        if value == scrollbar.minimum():
            print ('reached min')  # top/left end


    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        x, y = a0.x() +self.scroll_area.horizontalScrollBar().value(), a0.y() +self.scroll_area.verticalScrollBar().value()
        if BWindowWorker.IS_NEW_CREATE_MODE:

            if self.active_point:
                self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
                                                                      self.b_figure_worker.get_current_figure(), x,
                                                                  y)
        elif BWindowWorker.IS_SELECT_FIGURE_MODE:
            print('1 self.is_press_rb : ', self.is_press_rb)
            if self.is_press_rb:
                print('1 self.is_press_rb : ', self.is_press_rb)
                if self.select_point:
                    print('2 self.select_point : ', self.select_point)
                    self.select_point.set_x(x)
                    self.select_point.set_y(y)
                    self.reload_mat()
        self.update()

    def wheelEvent(self, event: QWheelEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        x = event.x()+self.scroll_area.horizontalScrollBar().value()
        y = event.y()+self.scroll_area.verticalScrollBar().value()
        if BWindowWorker.IS_SELECT_FIGURE_MODE:
            if self.selected_figure is not None:
                print('self.selected_figure is not None')
                self.b_figure_worker.set_not_active_figures_color_size()
                # self.selected_figure = self.b_figure_worker.get_selected_figure(x, y)
                # self.selected_figure.set_point_color_radius(5, (250, 250, 51))
                self.select_point = self.b_figure_worker.get_point_of_figure_by_coors(x, y,
                                                                                      self.selected_figure)
                if self.select_point:
                    self.select_point.set_color((153, 255, 51))
            elif event.button() == Qt.LeftButton:
                self.is_press_rb = True
                print('T1', self.is_press_rb)
                self.selected_figure = self.b_figure_worker.get_selected_figure(x, y)
                print('self.selected_figure : ', self.selected_figure)
                self.selected_figure.set_point_color_radius(5, (250, 250, 51))

        self.reload_mat()
        self.update()
        print('PRESSS')

    def mouseReleaseEvent(self, event: QMouseEvent):
        print('+self.scroll_area.x() ',self.scroll_area.verticalScrollBar().value())
        x = event.x()+self.scroll_area.horizontalScrollBar().value()
        y = event.y()+self.scroll_area.verticalScrollBar().value()
        if BWindowWorker.IS_NEW_MODE:
            print('!!!New mode')
            if BWindowWorker.IS_NEW_CREATE_MODE:
                if event.button() == Qt.LeftButton:
                    print('Left button ', x, y)
                    self.b_figure_worker.add_point(x, y)
                    print(x, y)
                    self.result_f_mat = self.b_area_drawer.get_result_mat(self.result_f_mat, self.b_figure_worker.get_current_figure())
                    self.temp_f_mat = self.result_f_mat
                    self.active_point = self.active_figure.get_last_point()
                    self.created_f_mat = np.copy(self.result_f_mat)

            # elif BWindowWorker.IS_SELECT_FIGURE_MODE:
                # print('Select+move mode')
                # if event.button() == Qt.LeftButton:
                #     self.is_press_rb = True
                #     print('T1', self.is_press_rb)
                #     self.selected_figure = self.b_figure_worker.get_selected_figure(x, y)
                #     print('self.selected_figure : ',self.selected_figure)
                # elif event.button() == Qt.NoButton and self.is_press_rb:
                #     pass
            elif BWindowWorker.ADD_BEZIER_MODE:
                print('ADD BEZIER TO POINT')
                old_point = self.select_point
                bcpoint = BCPoint(old_point.get_name(), old_point.get_x(), old_point.get_y(), old_point.get_x() + 5,
                                  old_point.get_y() + 5)
                self.b_figure_worker.get_current_figure().get_points()[5] = bcpoint
                BWindowWorker.ADD_BEZIER_MODE = False
            self.update()

    # def click_event_doer(self, event, x, y, flags, params=None):
    #     if BWindowWorker.IS_NEW_MODE:
    #         print('!!!New mode')
    #         if BWindowWorker.IS_NEW_CREATE_MODE:
    #             print('!!!!New create mode')
    #             if event == cv2.EVENT_LBUTTONDOWN:
    #                 self.b_figure_worker.add_point(x, y)
    #                 print(x, y)
    #                 self.result_f_mat = self.b_area_drawer.get_result_mat(self.result_f_mat,
    #                                                                       self.b_figure_worker.get_current_figure())
    #                 self.temp_f_mat = self.result_f_mat
    #                 self.active_point = self.active_figure.get_last_point()
    #                 self.created_f_mat = np.copy(self.result_f_mat)
    #             if event == cv2.EVENT_MOUSEMOVE and self.active_point:
    #                 self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
    #                                                                       self.b_figure_worker.get_current_figure(), x,
    #                                                                       y)
    #         elif BWindowWorker.IS_SELECT_FIGURE_MODE:
    #             print('Select+move mode')
    #             if event == cv2.EVENT_LBUTTONDOWN:
    #                 self.is_press_rb = True
    #                 print('T1', self.is_press_rb)
    #                 self.selected_figure = self.b_figure_worker.get_selected_figure(x, y)
    #             elif event == cv2.EVENT_MOUSEMOVE and self.is_press_rb:
    #                 print('Move mouse')
    #                 if self.select_point:
    #                     self.select_point.set_x(x)
    #                     self.select_point.set_y(y)
    #             elif event == cv2.EVENT_LBUTTONUP:
    #                 print('T2')
    #                 self.is_press_rb = False
    #                 print(self.is_press_rb)
    #
    #             if self.selected_figure is not None:
    #                 self.b_figure_worker.set_not_active_figures_color_size()
    #                 self.selected_figure.set_point_color_radius(5, (250, 250, 51))
    #                 self.select_point = self.b_figure_worker.get_point_of_figure_by_coors(x, y, self.selected_figure)
    #                 if self.select_point:
    #                     self.select_point.set_color((153, 255, 51))
    #
    #             self.reload_mat()
    #
    #             if BWindowWorker.ADD_BEZIER_MODE:
    #                 print('ADD BEZIER TO POINT')
    #                 old_point = self.select_point
    #                 bcpoint = BCPoint(old_point.get_name(), old_point.get_x(), old_point.get_y(), old_point.get_x() + 5,
    #                                   old_point.get_y() + 5)
    #                 self.b_figure_worker.get_current_figure().get_points()[5] = bcpoint
    #                 BWindowWorker.ADD_BEZIER_MODE = False

    def reload_mat(self):
        self.result_f_mat = self.b_area_drawer.get_full_result_mat(self.source_f_mat,
                                                                   self.b_figure_worker.get_figures())
        self.temp_f_mat = self.result_f_mat

    # def show_window(self, window_name):
    #     is_show = True
    #     cv2.namedWindow(window_name)
    #     image_width = self.result_mat.shape[1]
    #     locate_app_on_center_of_window(window_name, image_width)
    #     cv2.setMouseCallback(window_name, self.click_event_doer)
    #     while is_show:
    #         cv2.imshow(window_name, self.result_f_mat)
    #         key = cv2.waitKey(1)
    #         if key != -1:
    #             if key == ord('n'):
    #                 BWindowWorker.IS_NEW_MODE = True
    #             elif key == ord('j'):
    #                 self.esc_reset()
    #                 cv2.putText(self.result_f_mat, 'NEW create mode', (10, 30), self.font, 1, (0, 255, 0), 1,
    #                             cv2.LINE_AA)
    #                 BWindowWorker.IS_NEW_CREATE_MODE = True
    #                 self.init_new_figure()
    #             elif key == ord('s'):
    #                 cv2.putText(self.result_f_mat, 'Select mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
    #                 BWindowWorker.IS_SELECT_FIGURE_MODE = True
    #
    #             elif key == ord('b') and BWindowWorker.IS_SELECT_FIGURE_MODE and self.select_point:
    #                 print('RRRRRRR', self.select_point)
    #                 cv2.putText(self.result_f_mat, 'Bezie mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
    #                 BWindowWorker.ADD_BEZIER_MODE = True
    #                 print('ADD_BEZIER_MODE')
    #
    #             elif key == ord('\b') and BWindowWorker.IS_NEW_CREATE_MODE:
    #                 print('200')
    #                 cv2.putText(self.result_mat, 'Backspace mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
    #                             1, cv2.LINE_AA)
    #                 self.b_figure_worker.remove_last_figure_point()
    #                 self.reload_mat()
    #
    #             elif key == 27:
    #                 self.esc_reset()
    #                 # self.init_new_figure()
    #                 # self.result_f_mat = self.temp_f_mat
    #                 self.save_to_result_mat()
    #             elif key == ord('q'):
    #                 break
    #     cv2.destroyAllWindows()



    def esc_reset(self):
        BWindowWorker.IS_SELECT_FIGURE_MODE = False
        BWindowWorker.IS_NEW_CREATE_MODE = False
        self.selected_figure = None
        self.select_point = None
        self.b_figure_worker.set_not_active_figures_color_size()
        print(self.b_figure_worker.get_figures())
        self.result_f_mat = self.b_area_drawer.get_full_result_mat(self.source_f_mat,
                                                                   self.b_figure_worker.get_figures())
        self.temp_f_mat = self.result_f_mat

    def save_to_result_mat(self):
        self.result_f_mat = self.temp_f_mat

    def draw_text(self, text: str):
        cv2.putText(self.result_mat, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)

    def get_mat_of_all_figures(self):
        coors = None
        local_mat = np.copy(self.source_f_mat)
        for f_name in self.b_figure_worker.get_all_figure_name():
            coors = [[val.get_x(), val.get_y()] for val in self.b_figure_worker.get_figure_by_name(f_name).get_points()]
            local_mat = self.b_area_drawer.draw_figure_from_list_coors(coors, local_mat)
        return local_mat

    def create_active_mat(self):
        pass

    def init_new_figure(self):
        self.active_point = None
        figure_name2 = utils.get_random_name()
        self.b_figure_worker.create_figure(figure_name2)
        self.b_figure_worker.save_current_figure_to_bd()
        self.active_figure = self.b_figure_worker.get_current_figure()
        self.result_f_mat = np.copy(self.result_f_mat)

def locate_app_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    tt1 = [[1, 7], [3, 6], [5, 9]]
    zipped = zip(tt1, tt1[1:])
    print(list(zipped))
