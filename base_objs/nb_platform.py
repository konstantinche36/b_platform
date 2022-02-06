import cv2
from utils import utils
from base_objs.b_obj import BCPoint, BPoint, BFigure, BFigureWorker, BArea, BAreaWorker, BWindowWorker, BLayer, BMatBD, \
    BAreaDrawer

figure_name = utils.get_random_name()


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
        self.selected_point: BPoint = None
        self.last_selected_point: BPoint = None

        self.b_area = BArea(layers={'base_layer': BLayer(name='layer1', mat=mat)})
        self.b_area_worker = BAreaWorker('demo_Area_worker', self.b_area)
        self.b_figure_worker = BFigureWorker('demo_Figure_worker')
        self.b_area_drawer = BAreaDrawer(self.b_area_worker)

    def reload_mat(self):
        self.result_f_mat = self.b_area_drawer.get_full_result_mat(self.source_f_mat,
                                                                   self.b_figure_worker.get_figures(),self.dot_radius,self.line_width)
        self.temp_f_mat = self.result_f_mat

    def create_new_figure(self):
        new_figure: BFigure = self.b_figure_worker.create_figure(utils.get_random_name())
        print(new_figure.get_figure_name())
        self.b_figure_worker.save_figure_to_bd(new_figure)
        return new_figure

    def do_action(self, x, y, action):
        if action[0]:
            self.add_point(x, y)
        elif action[1]:
            self.select(x, y)
        else:
            print('Empty action')
        # self.b_figure_worker.set_not_active_figures_color_size()

    def select(self, x, y):
        self.selected_figure = self.select_figure_by_co(x, y)
        if self.selected_figure:
            print('selected figure', self.selected_figure)
            self.highlight_selected_figure()
            pass
        else:
            print('Not selected')




    def select_v2(self, x, y):
        if self.selected_figure is None:
            self.b_figure_worker.set_not_active_figures_color_size()
            self.selected_figure = self.select_figure_by_co(x, y)
            if self.selected_figure:
                self.highlight_selected_figure()
                print('Selected!!!')
                # self.highlight_selected_figure()
                if self.selected_point:
                    self.highlight_selected_point()
                    self.move_selected_point(x, y)
                else:
                    self.selected_point = self.select_point_by_co(x, y)
            else:
                print('Not selected!!!')
                # self.selected_figure = self.select_figure_by_co(x, y)
                # self.highlight_selected_figure()
            self.reload_mat()

    def simple_select(self, x, y) -> BFigure:
        return self.get_obj_by_co(x, y)

    def get_obj_by_co(self, x, y):
        if self.selected_figure:
            self.selected_point = self.select_point_by_co(x, y)
            return self.selected_point
        else:
            return self.select_figure_by_co(x, y)
        return None

    def select_point_by_co(self, x, y):
        self.b_figure_worker.get_selected_point(x, y, self.selected_figure)

    def co_pop_to_point(self, x, y):
        return self.b_figure_worker.get_selected_point(x, y, self.selected_figure)

    def select_figure_by_co(self, x, y):
        return self.b_figure_worker.get_selected_figure(x, y)

    def select_point_by_co(self, x, y):
        return self.b_figure_worker.get_selected_point(x, y, self.selected_figure)

    def highlight_selected_figure(self, color_of_selected_figure=(250, 250, 51), radius=5):
        print('Highlight figure!')
        self.selected_figure.set_point_color_radius(radius, color_of_selected_figure)

    def highlight_selected_point(self, color_of_selected_point=(153, 255, 51), radius=8):
        print('Highlight figure!')
        print(self.selected_point is None)
        self.selected_point.set_color(color_of_selected_point)
        self.selected_point.set_radius(radius)

    def move_selected_point(self, x, y):
        self.selected_point.set_x(x)
        self.selected_point.set_y(y)

    def delete_point_last_point(self):
        self.selected_figure.remove_last_point()
        self.reload_mat()

    def delete_point(self, point: BPoint):
        print(point is None)
        self.selected_figure.remove_point(point)
        self.reload_mat()

    def reset_selected_figure(self):
        self.b_figure_worker.set_not_active_figures_color_size()
        self.selected_figure = None

    def add_point(self, x, y):
        if self.selected_figure is None:
            self.selected_figure = self.create_new_figure()
        self.b_figure_worker.add_point(x, y, self.selected_figure)
        self.result_f_mat = self.b_area_drawer.get_result_mat(self.result_f_mat, self.selected_figure, self.dot_radius, self.line_width)

    def draw_clear_point(self, x, y):
        if self.active_point:
            self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
                                                                  self.b_figure_worker.get_current_figure(), x,
                                                                  y)

    def draw_temp_line(self, x, y):
        if self.selected_figure is not None:
            print('draw_temp_line!!! ')
            self.result_f_mat = self.b_area_drawer.draw_temp_line(self.temp_f_mat,
                                                                  self.selected_figure, x,
                                                                  y, line_width=self.line_width)

    def set_temp_line_width(self, temp_line_width):
        self.temp_line_width = temp_line_width

    def set_line_width(self, line_width):
        self.line_width = line_width


def locate_app_on_center_of_window(window_name, image_width: int):
    offset_x_y = utils.get_offset(utils.get_screen_size()[0], image_width)
    cv2.moveWindow(window_name, offset_x_y[0], offset_x_y[1])


if __name__ == '__main__':
    print('start')
    b_f = BPlatform(mat=None)
    print('finish')
