import cv2
import numpy as np
from utils import utils
from base_objs.b_obj import BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD, BAreaDrawer, BLayerWorker
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
        self.cur_mat = self.result_mat

        self.active_layer = None
        self.source_f_mat = base_mat
        self.temp_f_mat = base_mat
        self.result_f_mat = base_mat
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def click_event_doer(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_EDIT_FIGURE_MODE:
            print('IS_EDIT_MODE')
        elif BWindowWorker.IS_CREATE_FIGURE_MODE:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.result_f_mat = self.b_area_drawer.draw_line_and_point(x, y, self.active_layer.get_mat(), self.reset_line_params)
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
            self.active_figure = selected_figure
            if self.active_figure is not None:
                self.result_mat = self.b_area_drawer.draw_bold_figure_from_list_coors(
                    [[val.get_x(), val.get_y()] for val in self.active_figure.get_points()], self.result_mat)
                self.temp_mat = self.result_mat

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
                if key == ord('c'):
                    self.b_figure_worker.create_figure(figure_name)
                    self.b_figure_worker.save_current_figure_to_bd()
                    layer_name = self.b_figure_worker.get_current_figure().get_name()
                    cv2.putText(self.result_mat, 'Create mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    self.active_layer = self.b_layer_worker.create_layer(layer_name, np.copy(self.cur_mat))
                    self.b_layer_worker.add_layer(layer_name, self.active_layer)
                    self.result_f_mat = self.active_layer.get_mat()
                    BWindowWorker.IS_CREATE_FIGURE_MODE = True
                if key == ord('d'):
                    cv2.putText(self.result_mat, 'Create cur_mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE = True
                if key == ord('e'):
                    cv2.putText(self.result_mat, 'Edit mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True
                if key == ord('s'):
                    cv2.putText(self.result_mat, 'Select mode', (10, 30), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_SELECT_FIGURE_MODE = True
                    if self.active_figure is not None:
                        self.result_mat = self.b_area_drawer.draw_bold_figure_from_list_coors(
                            [[val.get_x(), val.get_y()] for val in self.active_figure.get_points()], self.layer_mat)
                        self.temp_mat = self.result_mat
                if key == ord('\b'):
                    cv2.putText(self.result_mat, 'Backspace mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                1, cv2.LINE_AA)
                    self.b_figure_worker.remove_last_figure_point()
                    print(self.b_figure_worker.get_all_figure_name())
                    for f_name in self.b_figure_worker.get_all_figure_name():
                        coors = [[val.get_x(), val.get_y()] for val in
                                 self.b_figure_worker.get_figure_by_name(f_name).get_points()]
                        print(coors)
                        self.result_mat = self.b_area_drawer.draw_figure_from_list_coors(coors, self.layer_mat)
                        self.temp_mat = self.result_mat
                        print(2, self.b_figure_worker.get_last_point())
                elif key == 27:
                    BWindowWorker.IS_EDIT_FIGURE_MODE = False
                    BWindowWorker.IS_CREATE_FIGURE_MODE = False
                    BWindowWorker.IS_SELECT_FIGURE_MODE = False
                    BWindowWorker.IS_NEW_FIGURE = True
                    self.reset_line_params = True
                    self.result_f_mat = self.temp_f_mat
                    self.result_f_mat = self.b_layer_worker.get_mat_from_list_layers()
                    print('SSS', self.result_f_mat.shape)
                elif key == ord('q'):
                    break
        cv2.destroyAllWindows()

    def draw_text(self, text: str):
        cv2.putText(self.result_mat, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)


def locate_app_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    # print(input('Press button'))
    l1 = [800, 900, 100]
    l2 = [x for x in l1 if x > 500]
    print(l2)
