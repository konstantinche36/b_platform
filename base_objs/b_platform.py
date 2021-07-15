import cv2
import numpy as np
from utils import utils
from base_objs.b_obj import BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD, BAreaDrawer


class BPlatform:
    REDRAW_MENU = False
    reset_line_params = None

    def __init__(self, windows_worker: BWindowWorker, b_area: BArea, b_area_worker: BAreaWorker,
                 b_figure_worker: BFigureWorker, name='Default_platform_name'):
        self.name = name
        self.windows_worker = windows_worker
        self.b_area = b_area
        self.b_area_worker = b_area_worker
        self.b_figure_worker = b_figure_worker
        self.b_area_drawer = BAreaDrawer()
        self.source_mat = self.b_area.get_mat()
        self.temp_mat = np.copy(self.source_mat)
        self.mark_create_figure_is_true = None

    def click_event_doer(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_EDIT_FIGURE_MODE:
            print('IS_EDIT_MODE')
        if BWindowWorker.IS_CREATE_FIGURE_MODE:
            print('IS_CREATE_MODE')
            if event == cv2.EVENT_LBUTTONDOWN:
                self.b_figure_worker.add_point(x, y)
                self.source_mat = self.b_area_drawer.draw_line_and_point(x, y, self.source_mat, self.reset_line_params)
                self.temp_mat = self.source_mat
                self.reset_line_params = False
            if event == cv2.EVENT_MOUSEMOVE:
                self.source_mat = self.b_area_drawer.show_line(x, y, self.temp_mat, self.reset_line_params)
                print('LAST')
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
        image_width = self.source_mat.shape[1]
        set_image_on_center_of_window(window_name, image_width)
        cv2.setMouseCallback(window_name, self.click_event_doer)
        while is_show:
            cv2.imshow(window_name, self.source_mat)
            key = cv2.waitKey(1)
            if key != -1:
                print('get_event')
                if key == ord('c'):
                    self.b_figure_worker.create_figure('test_figure')
                    self.b_figure_worker.save_current_figure_to_bd()
                    print('figure is create')
                    cv2.putText(self.source_mat, 'Create mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_FIGURE_MODE = True
                if key == ord('d'):
                    cv2.putText(self.source_mat, 'Create curve mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_CURVE_FIGURE_MODE = True
                if key == ord('e'):
                    cv2.putText(self.source_mat, 'Edit mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True
                if key == ord('\b'):
                    cv2.putText(self.source_mat, 'Backspace mode', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    self.b_area_drawer.delete_current_point()
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True
                elif key == 27:
                    for figure_name in self.b_figure_worker.get_list_figures_name():
                        print(self.b_figure_worker.get_figure_by_name(figure_name))
                    BWindowWorker.IS_EDIT_FIGURE_MODE = False
                    BWindowWorker.IS_CREATE_FIGURE_MODE = False
                    BWindowWorker.IS_NEW_FIGURE = True
                    print('ESC')
                    self.source_mat = self.temp_mat
                    self.reset_line_params = True
                elif key == ord('q'):
                    break
        cv2.destroyAllWindows()

    def draw_text(self, text: str):
        cv2.putText(self.source_mat, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)


def set_image_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    print(input('Press button'))
