import cairo
import numpy as np
import cv2
from numpy import ndarray
from itertools import count
import math


# WINDOW_NAME = 'Window01'

def generate_mat_from_image(image_path=None):
    if image_path is not None:
        t_surface = cairo.ImageSurface.create_from_png(image_path)
        return np.ndarray(shape=(t_surface.get_height(), t_surface.get_width(), 4), dtype=np.uint8,
                          buffer=t_surface.get_data())


class BObj:
    _ids = count(0)

    def __init__(self, name=None):
        self.id = next(self._ids)
        if name is None:
            self.name = 'def_name_' + str(self.id)
        else:
            self.name = name + '_' + str(self.id)

    def get_name(self):
        return self.name


class BPoint(BObj):
    B_POINT_NAME_PART = 'POINT_'

    def __init__(self, name, x, y):
        super().__init__(BPoint.B_POINT_NAME_PART + name)
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def __str__(self):
        return f'{self.name} x:{self.x}, y:{self.y}'


class BCPoint(BPoint):
    B_C_POINT_NAME_PART = 'CURVE_'

    def __init__(self, name, x, y, x_c=None, y_c=None):
        super().__init__(BCPoint.B_C_POINT_NAME_PART + name, x, y)
        self.x_c = x_c
        self.y_c = y_c

    def get_x_c(self):
        return self.x_c

    def get_y_c(self):
        return self.y_c

    def __str__(self):
        return super(BCPoint, self).__str__() + f' x_c:{self.x_c}, y_c:{self.y_c}'


class BFigure(BObj):
    B_FIGURE_NAME_PART = 'FIGURE_'

    def __init__(self, name: str, b_points: [BPoint] = None):
        super().__init__(BFigure.B_FIGURE_NAME_PART + name)
        if b_points is None:
            b_points = []
        self.b_points = b_points

    def add_new_point(self, x, y):
        self.b_points.append(BPoint('tt_' + self.get_name(), x, y))

    def get_points(self):
        return self.b_points

    def __str__(self):
        return f'{self.name}: \n'+'\t'+'\n\t'.join(str(x) for x in self.b_points)

    def get_figure_name(self):
        return self.name


class ArrayBD:

    def __init__(self):
        self.figures_bd = {}

    def add_item(self, figure: BFigure):
        print(figure.get_name(), '!!!!!!!!!!!!!!!!!!!!!!!')
        self.figures_bd[figure.get_name()] = figure

    def get_item(self, figure_name: str):
        # print(self.figures_bd)
        return self.figures_bd[figure_name]
        # self.figures_bd[figure.get_name()] = figure

    def print_bd_values(self):
        return list(self.figures_bd.keys())


class BFigureWorker(BObj):
    B_FIGURE_WORKER_NAME_PART = 'FIGURE_WORKER_'

    def __init__(self, name, figures_bd=None):
        super().__init__(BFigureWorker.B_FIGURE_WORKER_NAME_PART + name)
        self.figures_bd = ArrayBD()
        self.has_current_figure = False
        self.current_figure: BFigure = None
        self.obj_name = name

    def create_figure(self, figure_name: str):
        self.current_figure = BFigure(figure_name, None)
        print(f'create figure is True')

    def get_list_figures_name(self):
        return self.figures_bd.print_bd_values()

    def save_current_figure_to_bd(self):
        self.figures_bd.add_item(self.current_figure)

    # def create_new_figure2(self, x, y):
    #     self.current_figure = BFigure(self.obj_name, [BPoint(name=self.obj_name, x=x, y=y)])
    #     self.has_current_figure = True
    #     if self.figures_bd is None:
    #         self.figures_bd = ArrayFiguresBD()
    #     print(f'create figure is True')

    def add_point(self, x, y):
        print(f'function add_point val:{x} {y}')
        self.current_figure.add_new_point(x, y)
        # if not self.has_current_figure:
        #     self.create_new_figure(self.current_figure.get_figure_name(), x, y)
        # else:
        #     self.current_figure.add_new_point(x, y)

    def get_figure(self):
        return self.current_figure

    def get_figure_by_name(self, name: str) -> BFigure:
        # return ''
        return self.figures_bd.get_item(name)

    def print_figure(self, b_figure):
        print(self.current_figure.get_points())
        # # todo
        # pass


# class BFiguresBD:
#     def __init__(self, figures=None):
#         self.figures = figures
#
#     def add_figure(self, figure):
#         self.figures.append(figure)
#
#     def delete_figure(self, figure_name):
#         pass


class BLayer(BObj):
    B_LAYER_NAME_PART = 'LAYER_'

    def __init__(self, name, mat: ndarray, mats: [] = None):
        super().__init__(BLayer.B_LAYER_NAME_PART + name)
        self.mat = mat
        self.mats = mats
        self.width = mat.shape[1]
        self.height = mat.shape[0]

    def get_mat(self):
        return self.mat

    def set_mat(self, mat):
        self.mat = mat

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class BArea(BObj):
    B_AREA_NAME_PART = 'AREA_'

    def __init__(self, name='Area01', layers: [BLayer] = None):
        super().__init__(BArea.B_AREA_NAME_PART + name)
        self.layers = layers

    def get_base_layer(self) -> BLayer:
        return self.layers[0]

    def get_mat(self):
        return self.get_base_layer().get_mat()

    def set_mat(self, mat):
        return self.get_base_layer().set_mat(mat)


class BAreaWorker(BObj):
    B_AREA_WORKER_NAME_PART = 'AREA_WORKER_'

    def __init__(self, name, cur_b_area: BArea = None):
        super().__init__(BAreaWorker.B_AREA_WORKER_NAME_PART + name)
        self.cur_b_area = cur_b_area

    def set_current_area(self, b_area: BArea):
        self.cur_b_area = b_area

    def get_current_area(self):
        return self.cur_b_area

    def update_area(self, area: BArea, b_figure: BFigure):
        pass

    def get_mat(self, b_area: BArea):
        return b_area.get_mat()


class BAreaDrawer(BObj):
    base_color = (0, 0, 255)
    other_color = (0, 255, 255)
    base_line_width = 1
    other_line_width = .5  # .5

    def __init__(self):
        super().__init__()
        self.surface = None
        self.width, self.height = 0, 0
        self.ctx = None
        self.save_x, self.save_y = None, None  # point for to start line
        self.save_x2, self.save_y2 = None, None  # point for to start line
        self.save_curv_x1, self.save_curv_y1 = None, None  # point for curves
        self.save_curv_x2, self.save_curv_y2 = None, None  # point for curves
        self.x2, self.y2 = None, None  # point for to curv point2

    def init_b_area_drawer(self, mat):
        self.width = mat.shape[1]
        self.height = mat.shape[0]
        self.surface = cairo.ImageSurface.create_for_data(mat, cairo.FORMAT_ARGB32, mat.shape[1],
                                                          mat.shape[0])
        self.ctx = cairo.Context(self.surface)

    def show_line(self, x, y, mat, is_new_line):
        self.init_b_area_drawer(np.copy(mat))
        if self.save_x is not None and self.save_y is not None and not is_new_line:
            self.build_line(self.save_x, self.save_y, x, y)
        return self.create_mat_from_buf(self.surface.get_data())

    def draw_line_and_point(self, x, y, mat, is_new_line):
        self.init_b_area_drawer(mat)
        if self.save_x is not None and self.save_y is not None and not is_new_line:
            self.build_line(self.save_x, self.save_y, x, y)
        self.add_point_to_sur(x, y, (0, 255, 255))
        self.update_saved_x_y(x, y)
        return self.create_mat_from_buf(self.surface.get_data())

    def draw_curve_and_point(self, x, y, mat, is_new_line):
        self.init_b_area_drawer(mat)
        # if is_new_line:
        #     self.save_x, self.save_y, self.save_x2, self.save_y2, self.save_curv_x1, self.save_curv_y1, self.save_curv_x2, self.save_curv_y2 = None, None, None, None, None, None, None, None
        if self.save_x is None and self.save_y is None:
            self.save_x, self.save_y = x, y
            self.add_point_to_sur(x, y, self.base_color)
        elif self.save_curv_x1 is None and self.save_curv_y1 is None:
            self.save_curv_x1, self.save_curv_y1 = x, y
            self.add_point_to_sur(x, y, self.other_color, radius=3)
            self.add_line(self.save_x, self.save_y, x, y, self.other_color, self.other_line_width)
        elif self.save_x2 is None and self.save_y2 is None:
            self.save_x2, self.save_y2 = x, y
            self.add_point_to_sur(x, y, self.base_color)
        else:
            self.save_curv_x2, self.save_curv_y2 = x, y
            self.add_curve(self.save_x, self.save_y, self.save_curv_x1, self.save_curv_y1,
                           self.get_parallel_val(x, self.save_x2), self.get_parallel_val(y,
                                                                                         self.save_y2), self.save_x2,
                           self.save_y2)
            self.add_point_to_sur(self.get_parallel_val(x, self.save_x2), self.get_parallel_val(y, self.save_y2),
                                  self.other_color, radius=3)
            self.add_line(self.save_x2, self.save_y2, self.get_parallel_val(x, self.save_x2),
                          self.get_parallel_val(y, self.save_y2),
                          self.other_color, self.other_line_width)
            self.add_point_to_sur(x, y, self.other_color, radius=3)
            self.add_line(self.save_x2, self.save_y2, x, y, self.other_color,
                          self.other_line_width)
            self.save_x, self.save_y = self.save_x2, self.save_y2
            self.save_curv_x1, self.save_curv_y1 = x, y
            self.save_x2, self.save_y2 = None, None
        return self.create_mat_from_buf(self.surface.get_data())

    def edit_curve(self, x, y, mat, is_new_line):
        self.init_b_area_drawer(np.copy(mat))
        if is_new_line and self.save_x is not None and self.save_y is not None:
            self.draw_curve_and_point(x, y, mat, is_new_line)
            # self.add_line(self.save_x2, self.save_y2, x, y, self.other_color,
            #               self.other_line_width)
            self.save_x, self.save_y, self.save_x2, self.save_y2, self.save_curv_x1, self.save_curv_y1, self.save_curv_x2, self.save_curv_y2 = None, None, None, None, None, None, None, None
        if self.save_x2 is not None and self.save_y2 is not None:
            self.add_line(self.save_x2, self.save_y2, x, y, self.other_color,
                          self.other_line_width)
            self.add_curve(self.save_x,
                           self.save_y,
                           self.save_curv_x1,
                           self.save_curv_y1,
                           self.get_parallel_val(x, self.save_x2),
                           self.get_parallel_val(y, self.save_y2),
                           self.save_x2,
                           self.save_y2
                           )
        elif self.save_curv_x1 is not None and self.save_curv_y1 is not None:
            self.add_curve(self.save_x,
                           self.save_y,
                           self.save_curv_x1,
                           self.save_curv_y1,
                           x,
                           y,
                           x,
                           y
                           )
        elif self.save_x is not None and self.save_y is not None:
            self.add_line(self.save_x, self.save_y, x, y, self.other_color,
                          self.other_line_width)
        return self.create_mat_from_buf(self.surface.get_data())

    def delete_current_point(self):
        print('Is deleted')
        pass

    def add_point_to_sur(self, x, y, color, radius=5):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.arc(x, y, radius, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.fill_preserve()

    def update_saved_x_y(self, x, y):
        self.save_x, self.save_y = x, y

    def reset_saved_x_y(self):
        self.save_x, self.save_y = None, None

    def update_curves_saved_x_y(self, x, y):
        self.save_curv_x1, self.save_curv_y1 = x, y
        self.save_curv_x2, self.save_curv_y2 = x + x * (-1) + x, y + y * (-1) + y

    def get_parallel_val(self, val, base):
        return base + val * (-1) + base

    def add_line(self, x1, y1, x2, y2, color, line_width):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        # self.ctx.set_source_rgb(color)
        self.ctx.set_line_width(line_width)
        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.stroke()

    def add_curve(self, x, y, x1, y1, x2, y2, x3, y3):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x, y)
        self.ctx.curve_to(x1, y1, x2, y2, x3, y3)
        self.ctx.stroke()

    def build_line(self, x1, y1, x2, y2):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.stroke()

    def edit_curve_line(self, x, y, x1, y1, x2, y2, x3, y3):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x, y)
        self.ctx.curve_to(x1, y1, x2, y2, x3, y3)
        self.ctx.stroke()

    def edit_curve_line2(self, x1, y1, x2, y2):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x1, y1)
        self.ctx.curve_to(x1, y1, x2, y2, x2 + 100, y2 - 100)
        self.ctx.stroke()

    def build_curve_line(self, x1, y1, x2, y2):
        self.ctx.set_source_rgb(0, 0, 255)
        self.ctx.set_line_width(1)
        self.ctx.move_to(x1, y1)
        self.ctx.curve_to(self.save_curv_x1, self.save_curv_y1, x2, y2, self.save_curv_x2, self.save_curv_y2)
        self.ctx.stroke()

    def create_mat_from_buf(self, buf):
        l1 = np.ndarray(shape=(self.height, self.width, 4), dtype=np.uint8, buffer=buf)
        # print(l1.shape)
        return l1


class BMatBD:
    def __init__(self, mats):
        self.mats = mats

    def get_mats(self):
        return self.mats


class BAreaBD:
    def __init__(self, areas=None):
        self.areas = areas


class BWindowWorker:
    IS_EDIT_FIGURE_MODE = None
    IS_CREATE_FIGURE_MODE = None
    IS_NEW_FIGURE = None
    IS_CREATE_CURVE_FIGURE_MODE = None

    def __init__(self, window_name='Test window'):
        self.window_name = window_name

    def show_window(self, click_event, window_name, mat):
        is_show = True
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, click_event)
        while is_show:
            cv2.imshow(window_name, mat)
            key = cv2.waitKey(1)
            if key == ord('s'):
                BWindowWorker.IS_EDIT_MODE = True
            elif key == 27:
                BWindowWorker.IS_EDIT_MODE = False
                # self.img_mat = l2
            elif key == ord('q'):
                break
        cv2.destroyAllWindows()

    def get_window_name(self):
        return self.window_name


if __name__ == '__main__':
    b_f = BFigure('l1', [BPoint('p1', 1, 2), BPoint('p2', 3, 2)])
    # print(type(b_f.get_points()))
    print(b_f)

    b_c_f = BFigure('l1', [BCPoint('p1', 23, 45, 4, 3)])
    print(b_c_f)
