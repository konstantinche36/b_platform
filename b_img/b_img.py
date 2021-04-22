import numpy as np
import cv2
import cairo
import math
import sys

DEF_PATH = '/home/kostegan/work2021/scripts/b_platform/def_black_img.png'
DEF_HEIGHT = 400
DEF_WIDTH = 600
DEFAULT_IMG_FILL = np.zeros((DEF_HEIGHT, DEF_WIDTH, 3), np.uint8)
LIST_POINTS = []
DEF_IMG_PATH = ''
DEF_IMG_MAT = ''
WINDOW_NAME = 'Window01'
WINDOW_POSITION = (20, 30)
IMG_HEIGHT = 0
IMG_WIDTH = 0

sys.setrecursionlimit(10 ** 9)
bx1, by1, bx2, by2 = (None, None, None, None)
cur_x, cur_y = 0, 0
first_x, first_y  = 0 , 0


class BImage:
    def __init__(self, image_path=None):
        if image_path is None:
            image_path = '/home/kostegan/work2021/scripts/b_platform/def_black_img.png'
        self.image_path = image_path

    def get_image_path(self):
        # print(self.image_path)
        return self.image_path


class BImageWorker:
    def __init__(self, image=None):
        if image is None:
            image = BImage()
        self.img_path = image.get_image_path()
        self.img_mat = cv2.imread(image.get_image_path())
        self.img_height = self.img_mat.shape[0]
        self.img_width = self.img_mat.shape[1]
        self.b_figures = {}

    def configure_window_for_img(self):
        cv2.namedWindow(WINDOW_NAME)
        cv2.moveWindow(WINDOW_NAME, WINDOW_POSITION[0], WINDOW_POSITION[1])

    def resize_image_mat(self, scale_percent=100):
        scale_percent = scale_percent  # percent of original size
        width = int(self.img_mat.shape[1] * scale_percent / 100)
        height = int(self.img_mat.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        self.img_width, self.img_height = (width, height)
        self.img_mat = cv2.resize(self.img_mat, dim, interpolation=cv2.INTER_AREA)
        self.img_path = 'resize_' + self.img_path
        # cv2.imwrite(self.img_path, self.img_mat)
        cv2.imwrite(self.img_path, self.img_mat, [cv2.IMWRITE_PNG_COMPRESSION, 9])

    def show_image(self):
        cv2.setMouseCallback(WINDOW_NAME, self.click_event)
        # print('TTTTTTTTT')
        cv2.imshow(WINDOW_NAME, self.img_mat)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        while (1):
            cv2.imshow(WINDOW_NAME,  self.img_mat)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        global bx1, by1, bx2, by2, cur_x, cur_y, first_x, first_y
        # print(x, y)
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            first_x, first_y = x , y
            self.img_mat = self.b_figures.get('bezie01').draw_line(bx1, by1, bx2, by2)
            # print(x, y)
        if event == cv2.EVENT_MOUSEMOVE:
            cur_x, cur_y = x, y
            # print(f'LB_DOWN x - {x}, y - {y}, cur_x - {cur_x}, cur_y - {cur_y}')
            # if cur_x != x or cur_y != y:
            #     print(x, y)
            bx2, by2 = x, y
            # self.img_mat = self.b_figures.get('bezie01').draw_line(bx1, by1, bx2, by2)
            self.img_mat = self.b_figures.get('bezie01').show_line(None, None, bx2, by2,True,self.img_mat)
            # self.img_mat = self.b_figures.get('bezie01').draw_line(bx1, by1, bx2, by2)
            bx1, by1 = x, y
            # print(self.img_mat[0],' ',self.img_mat[1])
            # self.show_image()
        # if event == cv2.EVENT_MOUSEMOVE:
        #     print(f'LB_UP x - {x}, y - {y}, cur_x - {cur_x}, cur_y - {cur_y}')
        #     # while cur_x != x or cur_y != y:
        #     #     print(f'LB_UP x - {x}, y - {y}, cur_x - {cur_x}, cur_y - {cur_y}')
        #         # cur_x, cur_y = x , y

    def create_figure(self, name):
        self.b_figures[name] = BFigureWorker(name=name, img_path=self.img_path, source_mat=self.img_mat,
                                             mat_height=self.img_height,
                                             mat_width=self.img_width)

    def get_str_of_figures(self):
        result = ''
        for i, e in enumerate(list(self.b_figures.values())):
            result += f'\n\t figure {i} = {e.name}'
        return result

    def __str__(self):
        return f'... B\nObject of a class <BImageWorker> has:{self.get_str_of_figures()}\n...'

    def do_operation(self, obj, method):
        obj.method(self.img_mat)


class BFigureWorker:
    loc_x, loc_y = 0, 0

    def __init__(self, name, img_path, source_mat, mat_height, mat_width):
        self.surface = cairo.ImageSurface.create_from_png(img_path)
        self.copy_surface = cairo.ImageSurface.create_from_png(img_path)
        # self.surface = cairo.ImageSurface.create_from_png('test_img.png')
        self.source_mat = source_mat
        self.img_path = img_path
        self.mat_height = mat_height
        self.mat_width = mat_width
        self.ctx = cairo.Context(self.surface)
        self.name = name
        self.x1, self.y1, self.x2, self.y2 = (None, None, None, None)
        self.b_items = []

    def insert_local_cor(self, x, y):
        self.loc_x, self.loc_y = x, y

    def show_line(self, x1, y1, x2, y2, vall, data):
        # self.draw_point(x2, y2)
        # self.ctx.
        if first_x is not None and first_x != 0:
            # self.surface = self.copy_surface
            self.surface = cairo.ImageSurface.create_from_png(self.img_path)
            # self.surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, self.mat_width, self.mat_height)
            self.ctx = cairo.Context(self.surface)
            self.ctx.set_source_rgb(0, 0, 255)
            self.ctx.set_line_width(1)
            self.ctx.move_to(first_x, first_y)
            # self.ctx.line_to(x1 + 10, y1 + 10)
            self.ctx.line_to(x2, y2)
            if vall:
                self.ctx.stroke()
            self.loc_x, self.loc_y = x2, y2
            # if vall:
            #     self.surface = self.copy_surface
            # print('!!!!!!!!!!!!!!')
            # self.draw_point(x2, y2)
            print('Draw1')
        return self.create_mat_from_buf(self.surface.get_data())

    def commit_line(self, x1, y1, x2, y2):
        pass

    def draw_line(self, x1, y1, x2, y2):
        arr = None
        self.draw_point(x2, y2)
        if x1 is not None:
            self.ctx.set_source_rgb(0, 0, 255)
            self.ctx.set_line_width(1)
            self.ctx.move_to(x1, y1)
            # self.ctx.line_to(x1 + 10, y1 + 10)
            self.ctx.line_to(x2, y2)
            self.ctx.stroke()
            self.draw_point(x2, y2)
        # buf = self.surface.get_data()
        # arr = np.ndarray(shape=(self.mat_height, self.mat_width, 4), dtype=np.uint8, buffer=buf)
        # return arr if arr is not None else self.source_mat
        return self.create_mat_from_buf(self.surface.get_data())

    def draw_point(self, x, y):
        self.ctx.set_source_rgb(0, 255, 255)
        # self.ctx.set_line_width(9)
        # self.ctx.translate(x, y)
        self.ctx.arc(x, y, 5, 0, 2 * math.pi)
        # self.ctx.stroke_preserve()
        # cr.set_source_rgb(0.3, 0.4, 0.6)
        self.ctx.fill()
        # self.ctx.stroke()
        self.ctx.fill_preserve()
        # self.ctx.save()

    def create_mat_from_buf(self, buf):
        arr = np.ndarray(shape=(self.mat_height, self.mat_width, 4), dtype=np.uint8, buffer=buf)
        # print(arr.shape[0], ' ', arr.shape[1])
        return arr if arr is not None and arr.shape[0] > 0 and arr.shape[1] > 0 else self.source_mat


if __name__ == '__main__':
    # b_image_worker = BImageWorker()
    # b_image_worker.create_figure('bezie01')
    # b_image_worker.create_figure('bezie02')
    print(cv2.imread(DEF_PATH).shape)
    # b_image_worker.get_str_of_figures()
