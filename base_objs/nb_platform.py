import cv2
from utils import utils
from base_objs.b_obj import BCPoint, BPoint, BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BLayer, BMatBD, \
    BAreaDrawer

figure_name = utils.get_random_name()
ALL_BASE_FIGURE_COLOR = {
    'created_figures_point_color': (255, 255, 0),  # yellow
    'created_figures_line_color': (80, 80, 80),  # grey
    'selected_figures_point_color': (15, 255, 0),  # green
    'selected_figures_line_color': (0, 255, 255),  # cyan
    'selected_point_color': (255, 13, 0),  # red
    'deselected_figures_point_color': (0, 0, 255),  # blue
    'deselected_figures_line_color': (0, 0, 0),  # black
}


class BPlatform:
    REDRAW_MENU = False
    reset_line_params = None

    def __init__(self, mat):
        super().__init__()
        self.start_mat = mat
        self.result_f_mat = mat
        self.temp_f_mat = mat
        self.source_f_mat = mat
        self.active_figure: BFigure = None
        self.active_point: BPoint = None
        self.selected_figure: BFigure = None
        self.line_width = 1.5
        self.temp_line_width = 1
        self.dot_radius = 2.5
        self.selected_point: BCPoint = None
        self.last_selected_point: BPoint = None

        self.b_area = BArea(layers={'base_layer': BLayer(name='layer1', mat=mat)})
        self.b_area_worker = BAreaWorker('demo_Area_worker', self.b_area)
        self.b_figure_worker = BFigureWorker('demo_Figure_worker')
        self.b_area_drawer = BAreaDrawer(self.b_area_worker)

    def reload_mat(self):
        self.result_f_mat = self.b_area_drawer.get_full_result_mat(self.source_f_mat,
                                                                   self.b_figure_worker.get_figures(), self.dot_radius,
                                                                   self.line_width)
        self.temp_f_mat = self.result_f_mat

    def redraw_mat(self):
        self.result_f_mat = self.b_area_drawer.create_full_mat(self.source_f_mat, self.b_figure_worker.get_figures(),
                                                               self.selected_figure, self.selected_point,
                                                               self.dot_radius, self.line_width,
                                                               ALL_BASE_FIGURE_COLOR['selected_figures_line_color'],
                                                               ALL_BASE_FIGURE_COLOR['selected_figures_point_color'],
                                                               ALL_BASE_FIGURE_COLOR['selected_point_color'])
        self.temp_f_mat = self.result_f_mat

    def create_new_figure(self):
        new_figure: BFigure = self.b_figure_worker.create_figure(utils.get_random_name())
        self.b_figure_worker.save_figure_to_bd(new_figure)
        return new_figure

    def do_action(self, x, y, action):
        if action[0]:
            self.add_point(x, y)
        elif action[1]:
            self.select(x, y)
        elif action[2]:
            self.select(x, y)
            self.move(x, y)
        elif action[3]:
            self.select(x, y)
            self.add_curves_for_selected_point(x, y)
        elif action[4]:
            print('ADDED CURVE')
            # self.add_curve(x, y)
            # self.move(x, y)
            # self.edit_point(x, y)
        else:
            pass

    def add_curve(self, x, y):
        print('Add curve x y ', x, y)

    def select(self, x, y):
        if self.selected_point is None:
            self.selected_figure = self.select_figure_by_co(x, y)
            self.selected_point = self.select_point_by_co(x, y)

    def move(self, x, y):
        if self.selected_point:
            self.move_selected_point(x, y)

    def edit_point(self, x, y):
        if self.selected_point:
            print('DODODOD')
            self.add_curves_for_selected_point(x, y)

    def get_obj_by_co(self, x, y):
        if self.selected_figure:
            self.selected_point = self.select_point_by_co(x, y)
            return self.selected_point
        else:
            return self.select_figure_by_co(x, y)
        return None

    def co_pop_to_point(self, x, y):
        return self.b_figure_worker.get_selected_point(x, y, self.selected_figure, self.dot_radius)

    def select_figure_by_co(self, x, y):
        return self.b_figure_worker.get_selected_figure(x, y, self.dot_radius)

    def select_point_by_co(self, x, y):
        return self.b_figure_worker.get_selected_point(x, y, self.selected_figure, self.dot_radius)

    def move_selected_point(self, x, y):
        self.selected_point.set_x(x)
        self.selected_point.set_y(y)
        # if len(self.selected_point.coors) > 2:
        #     print('UPDATE XC YC')
        #     self.selected_point.update_x_c(x)
        #     print(self.selected_point)
        #     self.selected_point.update_y_c(y)

    def add_curves_for_selected_point(self, x, y):
        if self.selected_point:
            print('Added curve points!!!')
            self.selected_point.coors[2] = x
            self.selected_point.coors[3] = y
            if self.selected_point.last_coor_x_y() and self.selected_point.last_coor_x_y()[0] != x and \
                    self.selected_point.last_coor_x_y()[1] != y:
                x + x * (-1) + x, y + y * (-1) + y

    def delete_point_last_point(self):
        self.selected_figure.remove_last_point()
        self.reload_mat()

    def delete_point_from_figure(self, point: BPoint):
        self.selected_figure.remove_point(point)

    def add_point(self, x, y):
        if self.selected_figure is None:
            self.selected_figure = self.create_new_figure()
        self.b_figure_worker.add_curve_point(x, y, self.selected_figure)

    def draw_temp_line(self, x, y):
        if self.selected_figure is not None:
            self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
                                                                  self.selected_figure, x,
                                                                  y, line_width=self.line_width)

    def set_line_width(self, line_width):
        self.line_width = line_width


def locate_app_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    print('start')
    b_f = BPlatform(mat=None)
    print('finish')
