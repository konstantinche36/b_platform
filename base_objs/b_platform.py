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

        self.cur_mat = self.result_mat
        # self.b_layers_worker = BLayerWorker('base_layer', )

    def click_event_doer(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_EDIT_FIGURE_MODE:
            print('IS_EDIT_MODE')
        if BWindowWorker.IS_CREATE_FIGURE_MODE:
            # print('IS_CREATE_MODE')
            # print('00000000000000000000000' + str(len(self.b_layer_worker.layers)))
            if event == cv2.EVENT_LBUTTONDOWN:
                self.b_figure_worker.add_point(x, y)
                self.result_mat = self.b_area_drawer.draw_line_and_point(x, y,
                                                                         self.b_layer_worker.get_layer(
                                                                             self.b_figure_worker.get_current_figure().get_name()).get_mat(),
                                                                         self.reset_line_params)
                # todo передать нужный mat от слоя
                # self.result_mat = self.b_area_drawer.draw_line_and_point(x, y, self.b_area_worker.g self.reset_line_params)
                self.temp_mat = self.result_mat
                self.reset_line_params = False

            if event == cv2.EVENT_MOUSEMOVE:
                self.result_mat = self.b_area_drawer.show_line(x, y, self.temp_mat, self.reset_line_params)
                # print('LAST')
        if BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE:
            print('IS_CURVE_CREATE_MODE')
            # if event == cv2.EVENT_LBUTTONUP:
            #     # self.b_figure_worker.
            #     self.source_mat = self.b_area_drawer.draw_curve_and_point(x, y, self.temp_mat, self.reset_line_params)
            #     self.temp_mat = self.source_mat
            #     self.reset_line_params = False
            # if event == cv2.EVENT_MOUSEMOVE:
            #     self.source_mat = self.b_area_drawer.edit_curve(x, y, self.temp_mat, self.reset_line_params)

    def show_window(self, window_name):
        is_show = True
        cv2.namedWindow(window_name)
        image_width = self.result_mat.shape[1]
        locate_app_on_center_of_window(window_name, image_width)
        cv2.setMouseCallback(window_name, self.click_event_doer)
        while is_show:
            # cv2.imshow(window_name, self.result_mat)
            # cv2.imshow(window_name, self.b_area_worker.get_mat_from_list_layers())
            # print(type(self.b_layer_worker.get_mat_from_list_layers()))

            # cv2.imshow(window_name, self.cur_mat)
            cv2.imshow(window_name, self.result_mat)
            key = cv2.waitKey(1)
            if key != -1:
                # print('get_event')
                if key == ord('c'):
                    self.b_figure_worker.create_figure(figure_name)
                    self.b_figure_worker.save_current_figure_to_bd()
                    layer_name = self.b_figure_worker.get_current_figure().get_name()
                    print('layer_name: ',layer_name)
                    # print('figure is create')
                    cv2.putText(self.result_mat, 'Create mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1,
                                cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_FIGURE_MODE = True
                    self.b_layer_worker.add_layer(layer_name,
                                                  self.b_layer_worker.create_layer(layer_name, np.copy(self.cur_mat)))
                    # self.b_area_worker.create_layer(self.b_figure_worker.get_current_figure().get_name(),
                    #                                 # np.ndarray(shape=(1200, 900, 4)))
                    #                                 np.ndarray(shape=(1200, 900, 4), dtype=np.uint8))
                    # self.result_mat)
                    self.cur_mat = self.b_layer_worker.get_layer(layer_name).get_mat()
                if key == ord('d'):
                    cv2.putText(self.result_mat, 'Create curve mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE = True
                if key == ord('e'):
                    cv2.putText(self.result_mat, 'Edit mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1,
                                cv2.LINE_AA)
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True
                if key == ord('\b'):
                    cv2.putText(self.result_mat, 'Backspace mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                1, cv2.LINE_AA)
                    print(1, self.b_figure_worker.get_last_point())
                    self.b_figure_worker.remove_last_figure_point()
                    coors = [[val.get_x(), val.get_y()] for val in
                             self.b_figure_worker.get_current_figure().get_points()]
                    print(coors)
                    self.result_mat = self.b_area_drawer.draw_figure_from_list_coors(coors, self.layer_mat)
                    self.temp_mat = self.result_mat
                    print(2, self.b_figure_worker.get_last_point())
                    # self.b_area_drawer.delete_current_point()
                    # BWindowWorker.IS_EDIT_FIGURE_MODE = True
                elif key == 27:
                    # for figure_name in self.b_figure_worker.get_list_figures_name():
                    #     print(self.b_figure_worker.get_figure_by_name(figure_name))
                    # print(self.b_figure_worker.get_current_figure().get_points())
                    BWindowWorker.IS_EDIT_FIGURE_MODE = False
                    BWindowWorker.IS_CREATE_FIGURE_MODE = False
                    BWindowWorker.IS_NEW_FIGURE = True
                    print('ESC')
                    print(self.b_figure_worker.get_current_figure().get_points())
                    self.result_mat = self.temp_mat
                    self.reset_line_params = True
                    self.result_mat = self.b_layer_worker.get_mat_from_list_layers()
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
