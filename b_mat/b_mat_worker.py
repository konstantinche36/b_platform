import cv2
import cairo
import numpy as np


def create_black_mat(height: int, width: int):
    return np.zeros(shape=[width, height, 3], dtype=np.uint8)


def generate_mat_from_image(image_path=None):
    if image_path is not None:
        t_surface = cairo.ImageSurface.create_from_png(image_path)
        return np.ndarray(shape=(t_surface.get_height(), t_surface.get_width(), 4), dtype=np.uint8,
                          buffer=t_surface.get_data())


class BMatWorker:
    def __init__(self, name: str, width: int, height: int, fill: bool = False, fill_color=(255, 255, 255)):
        self.name = name
        self.width = width
        self.height = height
        self.fill = fill
        self.fill_color = fill_color

    def generate_fill_mat(self, width, height, fill_color=(255, 255, 255)):
        pass

    def generate_img_mat(self, path_to_img: str):
        pass

    def return_map_shape(self):
        pass

    @staticmethod
    def create_black_mat(height: int, width: int):
        return np.zeros(shape=[width, height, 4], dtype=np.uint8)


def show_map(mat):
    while True:
        cv2.imshow('test_window', mat)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break


def create_menu(width: int, height: int, option_name: str):
    l1 = create_black_mat(width, height)
    cv2.putText(l1, option_name, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(l1, 'Option 2', (15, 60), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(l1, 'Option 3', (15, 90), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    return l1


def add_menu_to_mat(base_mat, option_name):
    menu_mat = create_menu(400, 100, option_name)
    rows, cols, channels = menu_mat.shape
    roi = base_mat[0:rows, 0:cols]
    img2gray = cv2.cvtColor(menu_mat, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(menu_mat, menu_mat, mask=mask)
    dst = cv2.add(img1_bg, img2_fg)
    base_mat[0:rows, 0:cols] = dst
    return base_mat


if __name__ == '__main__':
    print('start')
    m1 = create_black_mat(200, 300)
    show_map(m1)
    print('end')
