import cv2
import numpy as np
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

    def click_event_doer(self):
        if BWindowWorker.IS_EDIT_MODE:
            print('IS_EDIT_MODE')
        if BWindowWorker.IS_EDIT_MODE:
            print('IS_CREATE_MODE')

    def click_event_for_b_window(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_EDIT_MODE:
            # self.windows_worker.add_text('')
            if event == cv2.EVENT_LBUTTONDOWN:
                self.b_figure_worker.add_point(x, y)
                self.source_mat = self.b_area_drawer.draw_line_and_point(x, y, self.source_mat)
                self.temp_mat = self.source_mat
            if event == cv2.EVENT_LBUTTONUP:
                print(x,y)
            if event == cv2.EVENT_MOUSEMOVE:
                self.source_mat = self.b_area_drawer.show_line(x, y, self.temp_mat)
        # elif BFigureWorker.IS_CREATE_MODE:
        #     pass

    def show_window(self, window_name):
        is_show = True
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.click_event_for_b_window)
        while is_show:
            cv2.imshow(window_name, self.source_mat)
            key = cv2.waitKey(1)
            if key == ord('c'):
                BWindowWorker.IS_CREATE_MODE = True
            if key == ord('s'):
                BWindowWorker.IS_EDIT_MODE = True
            elif key == 27:
                BWindowWorker.IS_EDIT_MODE = False
            elif key == ord('q'):
                break
        cv2.destroyAllWindows()
