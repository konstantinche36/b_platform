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
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# sys.setrecursionlimit(10 ** 9)
bx1, by1, bx2, by2 = (None, None, None, None)
cur_x, cur_y = 0, 0
first_x, first_y = None, None
second_x, second_y = None, None
l1, l2 = None, None


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
        global l1, l2
        if image is None:
            image = BImage()
        t_surface = cairo.ImageSurface.create_from_png(image.get_image_path())
        arr = np.ndarray(shape=(1200, 900, 4), dtype=np.uint8, buffer=t_surface.get_data())
        l1 = arr
        l2 = arr.copy()
        self.img_path = image.get_image_path()
        self.img_mat = arr
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
        # cv2.imshow(WINDOW_NAME, self.img_mat)
        while (1):
            cv2.imshow(WINDOW_NAME, self.img_mat)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, params):
        global bx1, by1, bx2, by2, cur_x, cur_y, first_x, first_y, second_x, second_y
        d = None
        if event == cv2.EVENT_LBUTTONDOWN:
            first_x, first_y = x, y
            self.img_mat = self.b_figures.get('bezie01').insert_point(x, y, self.img_mat)
            # self.img_mat = self.b_figures.get('bezie01').create_point(None, None, x, y, True, self.img_mat)
            # np.copyto(d,self.b_figures.get('bezie01').create_point(None, None, x, y, True, self.img_mat))
        if event == cv2.EVENT_MOUSEMOVE:
            # cur_x, cur_y = x, y
            self.img_mat = self.b_figures.get('bezie01').show_points(x, y, self.img_mat)

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
    x1_f, y1_f = None, None

    def __init__(self, name, img_path, source_mat, mat_height, mat_width):
        self.f_surface = cairo.ImageSurface.create_from_png(img_path)
        self.t_surface = cairo.ImageSurface.create_from_png(img_path)
        self.source_surface = cairo.ImageSurface.create_from_png(img_path)
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
        self.first_fig_x_point, self.first_fig_y_point = None, None
        self.second_fig_x_point, self.second_fig_y_point = None, None

    def insert_local_cor(self, x, y):
        self.loc_x, self.loc_y = x, y

    def insert_point(self, x, y, mat):
        global l2
        self.surface = cairo.ImageSurface.create_for_data(mat, cairo.FORMAT_ARGB32, self.mat_width,
                                                          self.mat_height)
        self.ctx = cairo.Context(self.surface)
        if self.first_fig_x_point is None and self.first_fig_y_point is None:
            self.first_fig_x_point, self.first_fig_y_point = x, y
            self.add_point_to_sur(x, y, CYAN)
            self.source_mat = mat.copy()
        else:
            l2 = mat
            self.second_fig_x_point, self.second_fig_y_point = x, y
            self.add_point_to_sur(x, y, RED)
            self.first_fig_x_point, self.first_fig_y_point = x, y
            self.second_fig_x_point, self.second_fig_y_point = None, None
        return self.create_mat_from_buf(self.surface.get_data())

    def show_points(self, x, y, mat):
        self.surface = cairo.ImageSurface.create_for_data(np.copy(l2), cairo.FORMAT_ARGB32, self.mat_width, self.mat_height)
        # self.surface = cairo.ImageSurface.create_for_data(l2, cairo.FORMAT_ARGB32, self.mat_width, self.mat_height)
        # self.surface = cairo.ImageSurface.create_from_png(self.img_path)
        print('p1')
        self.ctx = cairo.Context(self.surface)
        if self.first_fig_x_point is not None and self.first_fig_y_point is not None:
            self.build_line(self.first_fig_x_point, self.first_fig_y_point, x, y)
        print(f'{x} - {y}')
        print(np.array_equal(mat, self.source_mat))
        return self.create_mat_from_buf(self.surface.get_data())

    def build_line(self, x1, y1, x2, y2):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.stroke()

    def add_point_to_sur(self, x, y, color):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.arc(x, y, 5, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.fill_preserve()
        print('ok')

    def create_point(self, x1, y1, x2, y2, n1, n2):
        if first_x is not None and first_y is not None:
            self.x1_f, self.y1_f = first_x, first_y
            self.ctx.set_source_rgb(0, 0, 255)
            self.ctx.set_line_width(1)
            self.ctx.move_to(self.x1_f, self.y1_f)
            print(f'if {self.x1_f} {self.y1_f}')
            self.ctx.stroke()
            self.draw_point(self.x1_f, self.y1_f)
            # self.t_surface =
        return self.create_mat_from_buf(self.surface.get_data())

    def show_line_feature(self, x1, y1, x2, y2, n1, source_mat):
        data = source_mat
        print('source_mat')
        if first_x is not None and first_y is not None:
            # self.surface = cairo.ImageSurface.create_for_data(source_mat, cairo.FORMAT_ARGB32, self.mat_width,
            #                                                   self.mat_height)
            self.surface = cairo.ImageSurface.create_from_png(self.img_path)
            self.ctx = cairo.Context(self.surface)
            # self.x1_f, self.y1_f = first_x, first_y
            self.ctx.set_source_rgb(0, 0, 255)
            self.ctx.set_line_width(1)
            self.ctx.move_to(self.x1_f, self.y1_f)
            self.ctx.line_to(x2, y2)
            self.ctx.stroke()
            print('not_source_mat')
            data = self.create_mat_from_buf(self.surface.get_data())
        return data

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
        return self.create_mat_from_buf(self.surface.get_data())

    def draw_point(self, x, y):
        self.ctx.set_source_rgb(0, 255, 255)
        self.ctx.arc(x, y, 5, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.fill_preserve()

    def create_mat_from_buf(self, buf):
        arr = np.ndarray(shape=(self.mat_height, self.mat_width, 4), dtype=np.uint8, buffer=buf)
        return arr if arr is not None and arr.shape[0] > 0 and arr.shape[1] > 0 else self.source_mat


if __name__ == '__main__':
    # b_image_worker = BImageWorker()
    # b_image_worker.create_figure('bezie01')
    # b_image_worker.create_figure('bezie02')
    # print(cv2.imread(DEF_PATH).shape)
    # b_image_worker.get_str_of_figures()
    a = np.matrix('1 2; 3 4')
    b = a.copy()

    bb = np.array_equal(a,b)
    print(f'is equals {bb} --- {b}  -- {a}')
    b[0] = 0
    cc = np.array_equal(a, b)
    print(f'is equals {cc} --- {b}  -- {a}')

