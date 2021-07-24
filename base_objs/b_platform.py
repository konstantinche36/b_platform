import cv2
import numpy as np
from utils import utils
from base_objs.b_obj import BPoint, BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD, BAreaDrawer, \
    BLayerWorker
from numpy import ndarray

figure_name = utils.get_random_name()


class BPlatform:
    REDRAW_MENU = False
    reset_line_params = None

    def __init__(self, windows_worker: BWindowWorker, base_mat: ndarray, b_area: BArea, b_area_worker: BAreaWorker,
                 b_figure_worker: BFigureWorker, name='Default_platform_name'):
        self.name = name
        self.windows_worker = windows_worker
        self.b_area = b_area
        self.b_area_worker = b_area_worker
        self.b_figure_worker = b_figure_worker
        self.result_mat = self.b_area.get_base_mat()
        self.b_area_drawer = BAreaDrawer(self.b_area_worker)
        self.layer_mat = self.result_mat
        self.temp_mat = np.copy(self.result_mat)
        self.mark_create_figure_is_true = None
        self.b_layer_worker = BLayerWorker('default_worker', base_mat)
        self.active_figure: BFigure = None
        self.active_point: BPoint = None
        self.cur_mat = self.result_mat

        self.layer_mat = self.result_mat
        self.active_layer = None
        self.source_f_mat = base_mat
        self.temp_f_mat = base_mat
        self.result_f_mat = base_mat
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def click_event_doer(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_NEW_MODE:
            print('New mode')
            if BWindowWorker.IS_NEW_CREATE_MODE:
                print('New create mode')
                if event == cv2.EVENT_LBUTTONDOWN:
                    print('New create mode')
                    self.b_figure_worker.add_point(x, y)
                    print(x, y)
                    self.result_f_mat = self.b_area_drawer.get_result_mat(self.result_f_mat,
                                                                          self.b_figure_worker.get_current_figure())
                    self.temp_f_mat = self.result_f_mat
                if event == cv2.EVENT_MOUSEMOVE:
                    self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
                                                                          self.b_figure_worker.get_current_figure(), x,
                                                                          y)
        else:
            if BWindowWorker.IS_TEST_MODE and self.active_figure:
                print('Test mode')
                # self.get_mat_of_all_figures()
                # if event == cv2.EVENT_LBUTTONDOWN:
                #     self.b_figure_worker.add_point(x, y)
                #     self.result_f_mat = self.b_area_drawer.draw_line_and_point(x, y, self.active_layer.get_mat(),
                #                                                                self.reset_line_params)
                #     self.temp_f_mat = self.result_f_mat
                #     self.reset_line_params = False
                # if event == cv2.EVENT_MOUSEMOVE:
                #     self.result_f_mat = self.b_area_drawer.show_line(x, y, self.temp_f_mat, self.reset_line_params)

            elif BWindowWorker.IS_EDIT_FIGURE_MODE:
                self.active_point = self.b_figure_worker.get_selected_point(x, y, self.active_figure)
                if self.active_point is not None:
                    self.active_point.set_color((9, 255, 0))
                    self.active_point.set_radius(9)
                    self.result_f_mat = self.b_area_drawer.draw_bold_point(self.active_point,
                                                                           np.copy(self.result_f_mat))
                self.temp_f_mat = self.result_f_mat
                print('IS_EDIT_MODE')
            elif BWindowWorker.IS_CREATE_FIGURE_MODE:
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.b_figure_worker.add_point(x, y)
                    self.result_f_mat = self.b_area_drawer.draw_line_and_point(x, y, self.active_layer.get_mat(),
                                                                               self.reset_line_params)
                    self.temp_f_mat = self.result_f_mat
                    self.reset_line_params = False
                if event == cv2.EVENT_MOUSEMOVE:
                    self.result_f_mat = self.b_area_drawer.show_line(x, y, self.temp_f_mat, self.reset_line_params)

            elif BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE:
                print('IS_CURVE_CREATE_MODE')
            elif BWindowWorker.IS_SELECT_FIGURE_MODE:
                if event == cv2.EVENT_LBUTTONDOWN:
                    selected_figure = self.b_figure_worker.get_selected_figure(x, y)
                    self.active_figure = selected_figure

            elif event == cv2.EVENT_LBUTTONDOWN:
                selected_figure = self.b_figure_worker.get_selected_figure(x, y)
                print('SELECTED FIGURE', self.active_figure)
                # selected_point = self.b_figure_worker.get_selected_point(x, y, selected_figure)
                self.active_figure = selected_figure
                # self.active_point = selected_point
                self.b_figure_worker.set_current_figure(self.active_figure)
                if self.active_figure is not None:
                    self.result_f_mat = self.b_area_drawer.draw_bold_figure_from_list_coors(
                        [[val.get_x(), val.get_y()] for val in self.active_figure.get_points()],
                        np.copy(self.layer_mat))

        # # elif event == cv2.EV and self.active_point:
        # elif event == cv2.EVENT_MOUSEMOVE and self.active_point:
        #     self.active_point.set_x(x)
        #     self.active_point.set_y(y)
        #     self.result_f_mat = self.b_area_drawer.show_line(x, y, self.temp_f_mat, False)
        #     self.result_f_mat = self.b_area_drawer.draw_bold_point(self.active_point.get_x(),
        #                                                            self.active_point.get_y(),
        #                                                            np.copy(self.layer_mat))
        #     self.temp_f_mat = self.result_f_mat

        # self.create_active_mat()

    def show_window(self, window_name):
        is_show = True
        cv2.namedWindow(window_name)
        image_width = self.result_mat.shape[1]
        locate_app_on_center_of_window(window_name, image_width)
        cv2.setMouseCallback(window_name, self.click_event_doer)
        while is_show:
            cv2.imshow(window_name, self.result_f_mat)
            key = cv2.waitKey(1)
            if key != -1:
                if key == ord('n'):
                    BWindowWorker.IS_NEW_MODE = True
                elif key == ord('j'):
                    cv2.putText(self.result_mat, 'NEW create mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_NEW_CREATE_MODE = True
                    self.b_figure_worker.create_figure(figure_name)
                    self.b_figure_worker.save_current_figure_to_bd()

                    layer_name = self.b_figure_worker.get_current_figure().get_name()  # ?
                    self.active_layer = self.b_layer_worker.create_layer(layer_name, np.copy(self.layer_mat))  # ?
                    self.b_layer_worker.add_layer(layer_name, self.active_layer)  # ?
                    self.result_f_mat = self.active_layer.get_mat()

                elif key == ord('p') and self.active_figure:
                    cv2.putText(self.result_mat, 'Test Mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_TEST_MODE = True
                elif key == ord('c'):
                    self.b_figure_worker.create_figure(figure_name)
                    self.b_figure_worker.save_current_figure_to_bd()
                    layer_name = self.b_figure_worker.get_current_figure().get_name()
                    cv2.putText(self.result_mat, 'Create mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    self.active_layer = self.b_layer_worker.create_layer(layer_name, np.copy(self.layer_mat))
                    self.b_layer_worker.add_layer(layer_name, self.active_layer)
                    self.result_f_mat = self.active_layer.get_mat()
                    BWindowWorker.IS_CREATE_FIGURE_MODE = True
                    self.layer_mat = self.active_layer.get_mat()
                elif key == ord('d'):
                    cv2.putText(self.result_mat, 'Create cur_mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE = True
                elif key == ord('e'):
                    cv2.putText(self.result_mat, 'Edit mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True if self.active_figure else False
                elif key == ord('s'):
                    cv2.putText(self.result_mat, 'Select mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_SELECT_FIGURE_MODE = True
                    if self.active_figure is not None:
                        self.result_mat = self.b_area_drawer.draw_bold_figure_from_list_coors(
                            [[val.get_x(), val.get_y()] for val in self.active_figure.get_points()], self.layer_mat)
                        self.temp_mat = self.result_mat
                elif key == ord('\b'):
                    cv2.putText(self.result_mat, 'Backspace mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                1, cv2.LINE_AA)
                    self.b_figure_worker.remove_last_figure_point()
                    local_mat = self.get_mat_of_all_figures()
                    self.result_f_mat = local_mat
                    self.active_layer.set_mat(local_mat)
                    self.layer_mat = local_mat
                    self.temp_f_mat = self.result_f_mat
                elif key == 27:
                    BWindowWorker.IS_EDIT_FIGURE_MODE = False
                    BWindowWorker.IS_CREATE_FIGURE_MODE = False
                    BWindowWorker.IS_SELECT_FIGURE_MODE = False
                    BWindowWorker.IS_TEST_MODE = False
                    BWindowWorker.IS_NEW_MODE = False
                    BWindowWorker.IS_NEW_FIGURE = True
                    self.active_figure = None
                    self.reset_line_params = True
                    self.result_f_mat = self.temp_f_mat
                    print('SSS', self.result_f_mat.shape)
                elif key == ord('q'):
                    break
        cv2.destroyAllWindows()

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


def locate_app_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    tt1 = [[1, 7], [3, 6], [5, 9]]
    zipped = zip(tt1, tt1[1:])
    print(list(zipped))
