import cv2
from base_objs.b_obj import BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BMatBD


class BPlatform:
    def __init__(self, windows_worker: BWindowWorker, b_area: BArea, b_area_worker: BAreaWorker,
                 name='Default_platform_name'):
        self.name = name
        self.windows_worker = windows_worker
        self.b_area = b_area
        self.b_area_worker = b_area_worker

    def click_event_for_b_window(self, event, x, y, flags, params=None):
        if BWindowWorker.IS_EDIT_MODE:
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f'left_button_cor: {x, y}')
            if event == cv2.EVENT_MOUSEMOVE:
                print(f'mouse move: {x, y}')

    def show(self):
        self.windows_worker.show_window(self.click_event_for_b_window, self.b_area.get_name(), self.b_area.get_mat())
