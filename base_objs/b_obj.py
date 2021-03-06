import cairo
import numpy as np
import cv2
from numpy import ndarray
from itertools import count
import math
import time
from utils import utils


# def generate_mat_from_image(image_path=None):
#     if image_path is not None:
#         t_surface = cairo.ImageSurface.create_from_png(image_path)
#         return np.ndarray(shape=(t_surface.get_height(), t_surface.get_width(), 4), dtype=np.uint8,
#                           buffer=t_surface.get_data())

def p(val):
    print(val)


def current_milli_time():
    return round(time.time() * 1000)


def simple_show_mat(mat, file_name):
    # cv2.imshow('m22', mat)
    cv2.imwrite(file_name + str(current_milli_time()) + '.png', mat)
    # cv2.waitKey(1000)
    # key = cv2.waitKey(1)
    # while True:
    #     if key == 27:
    #         cv2.destroyAllWindows()
    #         break


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
    DEF_COLOR = (0, 0, 250)
    DEF_RADIUS = 3

    def __init__(self, name, x, y, color: (int, int, int) = DEF_COLOR, radius: int = DEF_RADIUS):
        super().__init__(BPoint.B_POINT_NAME_PART + name)
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_color(self, color: (int, int, int) = DEF_COLOR):
        self.color = color

    def get_color(self):
        return self.color

    def set_radius(self, radius: int = DEF_RADIUS):
        self.radius = radius

    def get_radius(self):
        return self.radius

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

    def set_x_c(self, x):
        self.x_c = x

    def set_y_c(self, y):
        self.y_c = y

    def __str__(self):
        return super(BCPoint, self).__str__() + f' x_c:{self.x_c}, y_c:{self.y_c}'


class BLayer(BObj):
    B_LAYER_NAME_PART = 'LAYER_'

    def __init__(self, name, mat: ndarray):
        super().__init__(BLayer.B_LAYER_NAME_PART + name)
        self.mat = mat
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


class BFigure(BObj):
    B_FIGURE_NAME_PART = 'FIGURE_'

    def __init__(self, name: str, b_points: [BPoint] = None):
        super().__init__(BFigure.B_FIGURE_NAME_PART + name)
        if b_points is None:
            b_points = []
        self.b_points = b_points
        # self.

    def set_point_color_radius(self, radius, color: (255, 255, 0)):
        if self.b_points:
            for point in self.b_points:
                point.set_color(color)
                point.set_radius(radius)

    def set_point_color(self, color: (255, 255, 0)):
        for point in self.b_points:
            point.set_color(color)

    def add_new_point(self, x, y):
        self.b_points.append(BPoint('tt_' + self.get_name(), x, y))

    def get_points(self) -> [BPoint]:
        return self.b_points

    def get_points(self, ) -> [BPoint]:
        return self.b_points

    def get_last_point(self) -> BPoint:
        return self.b_points[-1] if len(self.b_points) > 0 else None

    def __str__(self):
        return f'{self.name}: \n' + '\t' + '\n\t'.join(str(x) for x in self.b_points)

    def get_figure_name(self):
        return self.name

    def remove_last_point(self):
        if len(self.b_points) > 1:
            print(self.b_points.pop(len(self.b_points) - 1))

    def remove_point(self, point: BPoint):
        print('rem OK')

        for i in self.b_points:
            # print(point.get_x())
            # print('Type: ', type(i))
            if point.get_x() == i.get_x() and point.get_y() == i.get_y():
                self.b_points.remove(i)


class ArrayBD:

    def __init__(self):
        self.figures_bd = {}

    def add_item(self, figure: BFigure):
        self.figures_bd[figure.get_figure_name()] = figure

    def get_item(self, figure_name: str):
        # print(self.figures_bd)
        return self.figures_bd[figure_name]
        # self.figures_bd[figure.get_name()] = figure

    def print_bd_values(self):
        return list(self.figures_bd.keys())

    def get_all_name(self):
        return list(self.figures_bd.keys())

    def get_all_items(self) -> [BFigure]:
        return list(self.figures_bd.values())


class BFigureWorker(BObj):
    B_FIGURE_WORKER_NAME_PART = 'FIGURE_WORKER_'

    def __init__(self, name, figures_bd=None):
        super().__init__(BFigureWorker.B_FIGURE_WORKER_NAME_PART + name)
        self.figures_bd = ArrayBD()
        self.has_current_figure = False
        # self.current_figure: BFigure = None
        self.current_figure: BFigure = BFigure('test1')
        self.obj_name = name

    def actived_figure(self, figure: BFigure = None):
        if figure is not None:
            self.current_figure = figure
        return self

    def set_not_active_figures_color_size(self, color: (int, int, int) = (0, 0, 204), radius: int = 3):
        for figure in self.get_figures():
            for point in figure.get_points():
                point.set_color(color)
                point.set_radius(radius)

    def highlight_figure(self, figure: BFigure, colors, radius):
        figure.get_points()
        pass

    def set_current_figure(self, figure: BFigure):
        self.current_figure = figure

    def save_figure_to_bd(self, figure: BFigure):
        self.figures_bd.add_item(figure)

    def get_figures(self) -> [BFigure]:
        return self.figures_bd.get_all_items()

    def get_selected_point(self, x, y, figure: BFigure) -> BPoint:
        if figure is not None:
            for point in figure.get_points():
                if (point.get_x() - x) ** 2 + (point.get_y() - y) ** 2 <= 5 ** 2:
                    return point
        return None

    def get_point_of_figure_by_coors(self, x, y, figure: BFigure) -> BPoint:
        for point in figure.get_points():
            if self.is_coors_of_point(x, y, point.get_x(), point.get_y()):
                return point
        return None

    def get_selected_figure(self, x, y) -> BFigure:
        for figure in self.figures_bd.get_all_items():
            list_points_of_figure = figure.get_points()
            for point in list_points_of_figure:
                if self.is_coors_of_point(x, y, point.get_x(), point.get_y()):
                    # if (point.get_x() - x) ** 2 + (point.get_y() - y) ** 2 <= 5 ** 2:
                    return figure
            if self.check_coors_on_line(x, y, list_points_of_figure):
                return figure
        return None

    def is_coors_of_point(self, x, y, p_x, p_y):
        return (p_x - x) ** 2 + (p_y - y) ** 2 <= 10 ** 2

    def check_coors_on_line(self, x, y, points: [BPoint]):
        for p1, p2 in zip(points, points[1:]):
            if int(self.calc_dist_betw_two_point(p1.get_x(), p1.get_y(), p2.get_x(), p2.get_y())) == int(
                    self.calc_dist_betw_two_point(p1.get_x(), p1.get_y(), x, y) + self.calc_dist_betw_two_point(x, y,
                                                                                                                p2.get_x(),
                                                                                                                p2.get_y())):
                return True
        return False

    def calc_dist_betw_two_point(self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    def get_all_figure_name(self):
        return self.figures_bd.get_all_name()

    def remove_last_figure_point(self):
        self.current_figure.remove_last_point()

    def get_last_point(self) -> BPoint:
        return self.current_figure.get_points()[len(self.current_figure.get_points()) - 1] if len(
            self.current_figure.get_points()) - 1 > 0 else None
        # return self.figures_bd.get_item(self.get_list_figures_name()[len(self.get_list_figures_name())-1])

    def create_figure(self, figure_name: str):
        return BFigure(figure_name, None)

    def get_list_figures_name(self):
        return self.figures_bd.print_bd_values()

    def save_current_figure_to_bd(self):
        self.figures_bd.add_item(self.current_figure)

    # def add_point_v2(self, x, y):
    #     print(f'function add_point val:{x} {y}')
    #     self.current_figure.add_new_point(x, y)
    #     return self.current_figure

    # def add_point(self, x, y):
    #     print(f'function add_point val:{x} {y} 1111')
    #     self.current_figure.add_new_point(x, y)

    def add_point(self, x, y, figure: BFigure):
        print(f'function add_point val:{x} {y} 22222')
        figure.add_new_point(x, y)
        # self.current_figure.add_new_point(x, y)

    def get_current_figure(self):
        return self.current_figure

    def get_figure_by_name(self, name: str) -> BFigure:
        # return ''
        return self.figures_bd.get_item(name)

    # def print_figure(self, b_figure):
    #     print(self.current_figure.get_points())
    #     # # todo
    #     # pass


class BLayerWorker:
    def __init__(self, name: str, base_mat: ndarray):
        self.name = name
        self.base_layer = BLayer('base_mat', base_mat)
        self.layers = {'base_layer': self.base_layer}
        self.width, self.height = base_mat.shape[0], base_mat.shape[1]

    def get_base_layer(self):
        return self.base_layer

    def create_layer(self, name, mat: ndarray):
        return BLayer(name + '_mat', mat)

    def add_layer(self, name, layer: BLayer):
        self.layers[name] = layer

    def get_layer(self, name):
        return self.layers[name]

    def get_mat_from_layer(self, name):
        return self.layers[name].get_mat()

    def get_mat_from_list_layers(self):
        result_mat = self.get_base_layer().get_mat()
        for i, layer in enumerate(list(self.layers.values())[1:]):
            result_mat = self.merge_layers(result_mat, layer.get_mat())
        return result_mat

    def merge_layers(self, background_layer, foreground_layer):
        mask = cv2.cvtColor(cv2.GaussianBlur(cv2.split(foreground_layer)[3], (3, 3), 1), cv2.COLOR_GRAY2BGR)
        background_layer = background_layer[:, :, :3].astype(float)
        foreground_layer = foreground_layer[:, :, :3].astype(float)
        mask = mask.astype(float) / 255
        background_layer = cv2.multiply(1.0 - mask, background_layer)
        foreground_layer = cv2.multiply(mask, foreground_layer)
        out_image = cv2.add(background_layer, foreground_layer)
        return out_image / 255


class BArea(BObj):
    B_AREA_NAME_PART = 'AREA_'

    def __init__(self, name='Area01', layers: {str: BLayer} = None):
        super().__init__(BArea.B_AREA_NAME_PART + name)
        self.layers: {str: BLayer} = layers

    def get_base_layer(self) -> BLayer:
        # print(type(self.layers.values()))
        return list(self.layers.values())[0]

    def get_base_mat(self):
        return self.get_base_layer().get_mat()

    def set_base_mat(self, mat):
        self.get_base_layer().set_mat(mat)

    def get_layers(self) -> [BLayer]:
        return self.layers

    def add_layer(self, name, layer):
        self.layers[name] = layer


class BAreaWorker(BObj):
    B_AREA_WORKER_NAME_PART = 'AREA_WORKER_'

    def __init__(self, name, cur_b_area: BArea = None):
        super().__init__(BAreaWorker.B_AREA_WORKER_NAME_PART + name)
        self.cur_b_area = cur_b_area

    def create_layer(self, name, mat):
        layer = BLayer(name, mat)
        self.cur_b_area.add_layer(name, layer)

    def set_current_area(self, b_area: BArea):
        self.cur_b_area = b_area

    def get_current_area(self):
        return self.cur_b_area

    def update_area(self, area: BArea, b_figure: BFigure):
        pass

    def get_base_mat(self, b_area: BArea):
        return b_area.get_base_mat()

    def get_mat_from_list_layers(self):
        result_mat = self.cur_b_area.get_base_mat()
        # simple_show_mat(result_mat, 'f1')
        layers = list(self.cur_b_area.get_layers().values())
        for layer in layers[1:]:
            result_mat = self.merge_layers(result_mat, layer.get_mat())
        return result_mat

    def merge_layers(self, background_layer, foreground_layer):
        mask = cv2.cvtColor(cv2.GaussianBlur(cv2.split(foreground_layer)[3], (3, 3), 1), cv2.COLOR_GRAY2BGR)
        background_layer = background_layer[:, :, :3].astype(float)
        foreground_layer = foreground_layer[:, :, :3].astype(float)
        mask = mask.astype(float)  # / 255
        background_layer = cv2.multiply(1.0 - mask, background_layer)
        foreground_layer = cv2.multiply(mask, foreground_layer)
        out_image = cv2.add(background_layer, foreground_layer)
        return out_image / 255

    def create_mask(self, mat):
        img2gray = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 250, 255, cv2.THRESH_BINARY_INV)
        color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        color = cv2.GaussianBlur(color, (3, 3), 1)
        return color


class BAreaDrawer(BObj):
    base_color = (0, 0, 255)
    other_color = (0, 255, 255)
    base_line_width = 1
    other_line_width = .5  # .5

    def __init__(self, area_worker: BAreaWorker):
        super().__init__()
        self.base_mat = area_worker.get_base_mat(area_worker.get_current_area())
        self.surface = None
        self.width, self.height = 0, 0
        self.ctx = None
        self.save_x, self.save_y = None, None  # point for to start line
        self.save_x2, self.save_y2 = None, None  # point for to start line
        self.save_curv_x1, self.save_curv_y1 = None, None  # point for curves
        self.save_curv_x2, self.save_curv_y2 = None, None  # point for curves
        self.x2, self.y2 = None, None  # point for to curv point2

    def draw_bold_point(self, point, mat):
        # mat = utils.add_alpha_channel(mat)
        self.init_b_area_drawer(mat)
        self.add_bold_point(point.get_x(), point.get_y(), color=point.get_color(), radius=point.get_radius())
        return self.get_result_mat()

    def draw_bold_figure_from_list_coors(self, list_coors, mat):
        mat = utils.add_alpha_channel(mat)
        self.init_b_area_drawer(mat)
        x1, y1, x2, y2 = None, None, None, None
        for coors_pars in list_coors:
            self.add_bold_point(coors_pars[0], coors_pars[1])
            if x1 is not None and y1 is not None:
                self.add_s_line(x1, y1, coors_pars[0], coors_pars[1])
            x1, y1 = coors_pars[0], coors_pars[1]
            # self.update_saved_x_y(coors_pars[0], coors_pars[1])
            # self.update_saved_x_y(coors_pars[0], coors_pars[1])
            # mat_res = self.draw_line_and_point(coors_pars[0], coors_pars[1], mat, False)
        self.update_saved_x_y(list_coors[-1][0] if len(list_coors) > 0 else None,
                              list_coors[-1][1] if len(list_coors) > 0 else None)
        return self.get_result_mat()

    def draw_cur_figure_from_points(self, points):

        pass

    def draw_figure_from_list_coors(self, list_coors, mat):
        self.init_b_area_drawer(np.copy(mat))
        # for coors_pars in reversed(list_coors):
        x1, y1, x2, y2 = None, None, None, None
        for coors_pars in list_coors:
            self.add_point(coors_pars[0], coors_pars[1])
            if x1 is not None and y1 is not None:
                self.add_s_line(x1, y1, coors_pars[0], coors_pars[1])
            x1, y1 = coors_pars[0], coors_pars[1]
            # self.update_saved_x_y(coors_pars[0], coors_pars[1])
            # self.update_saved_x_y(coors_pars[0], coors_pars[1])
            # mat_res = self.draw_line_and_point(coors_pars[0], coors_pars[1], mat, False)
        self.update_saved_x_y(list_coors[-1][0] if len(list_coors) > 0 else None,
                              list_coors[-1][1] if len(list_coors) > 0 else None)
        return self.get_result_mat()

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

    # def move_point(self, x, y ,mat,point:BPoint):
    #     self.init_b_area_drawer(np.copy(mat))
    #     # self.
    #     return self.create_mat_from_buf(self.surface.get_data())

    def draw_line_and_point(self, x, y, mat, is_new_line):
        self.init_b_area_drawer(mat)
        if self.save_x is not None and self.save_y is not None and not is_new_line:
            self.build_line(self.save_x, self.save_y, x, y)
        self.add_point_to_sur(x, y, (0, 255, 255))
        self.update_saved_x_y(x, y)
        return self.create_mat_from_buf(self.surface.get_data())

    def init_mat(self, mat):
        self.init_b_area_drawer(mat)

    def add_point(self, x, y):
        self.add_point_to_sur(x, y, (0, 255, 255))

    def add_bold_point(self, x, y, color=(255, 0, 0), radius=5):
        self.add_point_to_sur(x, y, color, radius=radius)

    def add_s_line(self, x1, y1, x2, y2):
        self.build_line(x1, y1, x2, y2)

    def draw_temp_line(self, mat: ndarray, figure: BFigure, x, y, line_width):
        self.init_b_area_drawer(np.copy(mat))
        if len(figure.get_points()) > 0:
            self.add_temp_line(figure.get_points()[-1], x, y, line_width=line_width)
            self.add_temp_point(figure.get_points()[-1], x, y)
        return self.create_mat_from_buf(self.surface.get_data())

    def get_full_result_mat(self, mat: ndarray, figures: [BFigure], dot_radius, line_width):
        self.init_b_area_drawer(np.copy(mat))
        for figure in figures:
            if figure is not None:
                # coors = [[point.get_x(), point.get_y()] for point in figure.get_points()]
                if len(figure.get_points()) > 0:
                    self.add_lines(figure.get_points(), line_width=line_width)
                    self.add_points(figure.get_points(), radius=dot_radius)
        return self.create_mat_from_buf(self.surface.get_data())

    def create_full_mat(self, base_mat: ndarray, figures: [BFigure], selected_figure, selected_points: [BPoint],
                        dot_radius, line_width, selected_line_color, selected_points_color, selected_point_color):
        self.init_b_area_drawer(np.copy(base_mat))
        for figure in figures:
            if figure is not None:
                if len(figure.get_points()) > 0:
                    self.add_lines(figure.get_points(), line_width=line_width)
                    self.add_points(figure.get_points(), radius=dot_radius)
        if selected_figure is not None:
            if len(figure.get_points()) > 0:
                self.add_lines(selected_figure.get_points(), line_width=line_width, color=selected_line_color)
                self.add_points(selected_figure.get_points(), radius=dot_radius, color=selected_points_color)
                if selected_points is not None:
                    self.add_points([selected_points], radius=dot_radius + 1, color=selected_point_color)
        return self.create_mat_from_buf(self.surface.get_data())

    def get_result_mat(self, mat: ndarray, figure: BFigure, radius, line_width):
        self.init_b_area_drawer(np.copy(mat))
        if figure is not None:
            # coors = [[point.get_x(), point.get_y()] for point in figure.get_points()]
            self.add_lines(figure.get_points(), line_width=line_width)
            self.add_points(figure.get_points(), radius=radius)
        return self.create_mat_from_buf(self.surface.get_data())

    # def get_result_mat(self):
    #     return self.create_mat_from_buf(self.surface.get_data())

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

    def add_point_to_sur(self, x, y, color, radius=3):
        self.ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
        self.ctx.arc(x, y, radius, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.fill_preserve()

    def add_points(self, points: [BPoint], radius, color=None):
        for point in points:
            if color is None:
                self.ctx.set_source_rgb(point.get_color()[0] / 255.0, point.get_color()[1] / 255.0,
                                        point.get_color()[2] / 255.0)
            else:
                self.ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0,
                                        color[2] / 255.0)
            self.ctx.arc(point.get_x(), point.get_y(), radius, 0, 2 * math.pi)
            self.ctx.fill()
        self.ctx.fill_preserve()

    def add_lines(self, points, color=(35 / 255.0, 45 / 255.0, 15 / 255.0), line_width=2):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(line_width)
        self.ctx.move_to(points[0].get_x(), points[0].get_y())
        for point in points[1:]:
            self.ctx.line_to(point.get_x(), point.get_y())
        self.ctx.stroke()

    # def add_lines(self, points, color=(35 / 255.0, 45 / 255.0, 15 / 255.0), line_width=2):
    #     self.ctx.set_source_rgb(color[0], color[1], color[2])
    #     self.ctx.set_line_width(line_width)
    #     self.ctx.move_to(points[0].get_x(), points[0].get_y())
    #     for point in points[1:]:
    #         self.ctx.line_to(point.get_x(), point.get_y())
    #     self.ctx.stroke()

    def add_temp_line(self, last_point: BPoint, x, y, color=(12 / 255.0, 140 / 255.0, 200 / 255.0), line_width=2):
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(line_width)
        self.ctx.move_to(last_point.get_x(), last_point.get_y())
        self.ctx.line_to(x, y)
        self.ctx.stroke()

    def add_temp_point(self, last_point: BPoint, x, y):
        pass

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
        # self.ctx.move_to(x1+5, y1+10)
        # self.ctx.line_to(x2+20, y2+15)
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
    IS_SELECT_FIGURE_MODE = None
    IS_TEST_MODE = None
    IS_NEW_MODE = None
    IS_NEW_CREATE_MODE = None
    IS_ESC_RESET_MODE = None
    ADD_BEZIER_MODE = None

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
    f = BFigure('l1', [BPoint('p1', 1, 3), BPoint('p2', 5, 3), BPoint('p3', 6, 2)])
    print(f)

    (x - x0) ** 2 + (y - y0) ** 2 <= 5 ** 2
