import cairo
import numpy as np
import cv2
from numpy import ndarray
from itertools import count


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
        return f'x:{self.x}, y:{self.y}'


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
        self.b_points.append(BPoint('tt' + self.get_name(), x, y))

    def get_points(self):
        return self.b_points

    def __str__(self):
        return ', '.join(str(x) for x in self.b_points)


class BFigureWorker(BObj):
    B_FIGURE_WORKER_NAME_PART = 'FIGURE_WORKER_'

    def __init__(self, name, figures_bd=None):
        super().__init__(BFigureWorker.B_FIGURE_WORKER_NAME_PART + name)
        self.figures_bd = figures_bd
        self.has_current_figure = False
        self.current_figure: BFigure = None
        self.obj_name = name

    def create_new_figure(self, x, y):
        self.current_figure = BFigure(self.obj_name, [BPoint(name=self.obj_name, x=x, y=y)])
        self.has_current_figure = True
        print(f'create figure is True')

    def add_point(self, x, y):
        print(f'function add_point val:{x} {y}')
        if not self.has_current_figure:
            self.create_new_figure(x, y)
        else:
            self.current_figure.add_new_point(x, y)

    def get_figure(self):
        return self.current_figure

    def print_figure(self, b_figure):
        print(self.current_figure.get_points())
        # # todo
        # pass


class BFiguresBD:
    def __init__(self, figures=None):
        self.figures = figures

    def add_figure(self, figure):
        self.figures.append(figure)

    def delete_figure(self, figure_name):
        pass


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


class BAreaWorker(BObj):
    B_AREA_WORKER_NAME_PART = 'AREA_WORKER_'

    def __init__(self, name, cur_b_area: BArea = None):
        super().__init__(BAreaWorker.B_AREA_WORKER_NAME_PART + name)
        self.cur_b_area = cur_b_area

    def set_current_area(self, b_area: BArea):
        self.cur_b_area = b_area

    def get_current_area(self):
        return self.cur_b_area

    def update_area(self, area: BArea):
        pass

    def get_mat(self, b_area: BArea):
        return b_area.get_mat()


class BMatBD:
    def __init__(self, mats):
        self.mats = mats

    def get_mats(self):
        return self.mats


class BAreaBD:
    def __init__(self, areas=None):
        self.areas = areas


class BWindowWorker:
    IS_EDIT_MODE = None

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
