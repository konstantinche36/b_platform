import cairo
import numpy as np
import cv2


def generate_mat_from_image(image_path=None):
    if image_path is not None:
        t_surface = cairo.ImageSurface.create_from_png(image_path)
        return np.ndarray(shape=(t_surface.get_height(), t_surface.get_width(), 4), dtype=np.uint8,
                          buffer=t_surface.get_data())


class BObj:
    def __init__(self, name=None):
        if name is None:
            self.name = 'Default layer'
        self.name = name

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


class BFigure(BObj):
    B_FIGURE_NAME_PART = 'FIGURE_'

    def __init__(self, name, b_points=None):
        super().__init__(BFigure.B_FIGURE_NAME_PART + name)
        if b_points is None:
            b_points = []
        self.b_points = b_points


class BFigureWorker(BObj):
    B_FIGURE_WORKER_NAME_PART = 'FIGURE_WORKER_'

    def __init__(self, name='Worker', figures_bd=None):
        super().__init__(BFigureWorker.B_FIGURE_WORKER_NAME_PART + name)
        self.figures_bd = figures_bd


class BFiguresBD:
    def __init__(self, figures=None):
        self.figures = figures

    def add_figure(self, figure):
        self.figures.append(figure)

    def delete_figure(self, figure_name):
        pass


class BAreaWorker(BObj):
    B_AREA_WORKER_NAME_PART = 'AREA_WORKER_'

    def __init__(self, name, areas_bd=None):
        super().__init__(BAreaWorker.B_AREA_WORKER_NAME_PART + name)
        self.areas_bd = areas_bd

    def get_mat(self):
        return


class BMatBD:
    def __init__(self, mats):
        self.mats = mats

    def get_mats(self):
        return self.mats


class BAreaBD:
    def __init__(self, areas=None):
        self.areas = areas


class BArea(BObj):
    B_AREA_NAME_PART = 'AREA_'

    def __init__(self, name='Area01', image_path=None):
        super().__init__(BArea.B_AREA_NAME_PART + name)
        self.mat = generate_mat_from_image(image_path)
        self.width = self.mat.shape[1]
        self.height = self.mat.shape[0]

    def get_mat(self):
        return self.mat


class BLayer(BObj):
    B_LAYER_NAME_PART = 'LAYER_'

    def __init__(self, name):
        super().__init__(BLayer.B_LAYER_NAME_PART + name)


class BWindowShower:
    def __init__(self, window_name='Test window'):
        self.window_name = window_name

    def show_window(self, mat):
        is_show = True
        while is_show:
            cv2.imshow(self.window_name, mat)
            key = cv2.waitKey(3)
            if key == 27:
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    b_point = BPoint('l1', 21, 10)
    print(
        f'name: {b_point.get_name()}, coords: {b_point.get_x()}X{b_point.get_y()}'
    )
    b_c_point = BCPoint('l1', 3, 4)
    print(
        f'name: {b_c_point.get_name()}, coords: {b_c_point.get_x()}X{b_c_point.get_y()},{b_c_point.get_x_c()}X{b_c_point.get_y_c()}')
    b_figure = BFigure('f1')
    print(b_figure.get_name())
    # b_area = BArea('Area_01', '../resize_test_img.png')
    # print(f'area_name:{b_area.name}, area_height_width:{b_area.height}x{b_area.width}')
    # b_shower = BWindowShower(b_area.get_mat(), 'Win1')
    # b_shower.show_window()
    # # print('start __main__')
    # # mat = generate_mat_from_image('../resize_test_img.png')
    # # print(f'type: {type(mat)} shape: {mat.shape}')
