import pyautogui
import time
import numpy as np
import cv2

def add_alpha_channel(mat:np.ndarray):
    width, height, channels = mat.shape
    if channels == 3:
        alpha = np.zeros((width, height, 1), np.uint8)
        print('TT', alpha.shape)
        b_channel, g_channel, r_channel = cv2.split(mat)
        mat = cv2.merge((b_channel, g_channel, r_channel, alpha/255))
    return mat

def get_screen_size() -> (int, int):
    width, height = pyautogui.size()
    return width, height


def get_center(screen_size: int) -> int:
    center = screen_size / 2
    return int(center)


def get_offset(width_screen_size: int, width_image_size: int) -> (int, int):
    x_offset = 0
    y_offset = 20
    print(type(width_screen_size), type(width_image_size))
    if width_screen_size >= width_image_size:
        x_offset = get_center(width_screen_size) - get_center(width_image_size)
    return x_offset, y_offset


def current_milli_time():
    return round(time.time() * 1000)


def get_random_name():
    return 'test_name' + str(current_milli_time())
