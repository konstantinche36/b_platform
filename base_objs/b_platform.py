from base_objs.b_obj import BWindowShower, BMatBD, BFigure


class BPlatform:
    def __init__(self, windows_shower: BWindowShower, b_mat_bd: BMatBD, name='Default_platform_name'):
        self.name = name
        self.b_mat_bd = b_mat_bd
        self.windows_shower = windows_shower

    def show(self):
        self.windows_shower.show_window(self.b_mat_bd.get_mats()[0])

    def draw(self,b_figure: BFigure):
        pass
