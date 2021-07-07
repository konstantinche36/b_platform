import cv2
import numpy as np
from utils import utils
from base_objs.b_obj import BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD, BAreaDrawer


class BPlatform:
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
            if self.mark_create_figure_is_true:
                print('edit_figure')
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.b_figure_worker.add_point(x, y)
                    self.source_mat = self.b_area_drawer.draw_line_and_point(x, y, self.source_mat)
                    self.temp_mat = self.source_mat
                if event == cv2.EVENT_LBUTTONUP:
                    print(x, y)
                if event == cv2.EVENT_MOUSEMOVE:
                    self.source_mat = self.b_area_drawer.show_line(x, y, self.temp_mat)
            else:
                print('CREATE_FIGURE')
                self.b_figure_worker.create_new_figure(x, y)
                self.mark_create_figure_is_true = True

    # def click_event_for_b_window(self, event, x, y, flags, params=None):
    #     if BWindowWorker.IS_EDIT_FIGURE_MODE:
    #         # self.windows_worker.add_text('')
    #         if event == cv2.EVENT_LBUTTONDOWN:
    #             self.b_figure_worker.add_point(x, y)
    #             self.source_mat = self.b_area_drawer.draw_line_and_point(x, y, self.source_mat)
    #             self.temp_mat = self.source_mat
    #         if event == cv2.EVENT_LBUTTONUP:
    #             print(x, y)
    #         if event == cv2.EVENT_MOUSEMOVE:
    #             self.source_mat = self.b_area_drawer.show_line(x, y, self.temp_mat)
    #     # elif BFigureWorker.IS_CREATE_MODE:
    #     #     pass

    def show_window(self, window_name):
        is_show = True
        cv2.namedWindow(window_name)
        image_width = self.source_mat.shape[1]
        set_image_on_center_of_window(window_name, image_width)
        cv2.setMouseCallback(window_name, self.click_event_doer)
        font = cv2.FONT_HERSHEY_SIMPLEX
        while is_show:
            cv2.imshow(window_name, self.source_mat)
            key = cv2.waitKey(1)
            if key != -1:
                print('get_event')
                if key == ord('c'):
                    cv2.putText(self.source_mat, 'Christmas', (10, 450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
                    BWindowWorker.IS_CREATE_FIGURE_MODE = True
                if key == ord('s'):
                    cv2.putText(self.source_mat, 'Christmas1', (10, 450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
                    BWindowWorker.IS_EDIT_FIGURE_MODE = True
                elif key == 27:
                    BWindowWorker.IS_EDIT_FIGURE_MODE = False
                    BWindowWorker.IS_CREATE_FIGURE_MODE = False
                    self.mark_create_figure_is_true = False
                elif key == ord('q'):
                    break
        cv2.destroyAllWindows()


def set_image_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    a = None
    if a:
        print(200)
