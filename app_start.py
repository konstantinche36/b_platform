from base_objs.b_obj import BWindowWorker, BAreaWorker, BFigureWorker, BArea, BLayer
from base_objs.b_platform import BPlatform
from b_mat.b_mat_worker import generate_mat_from_image
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QScrollArea
import sys

if __name__ == '__main__':
    print('start!!!')
    # path = '/home/kostegan/work2021/scripts/b_platform/resize_test_img.png'
    path = '/home/kos/py_work_2021/b_platform/resize_test_img.png'

    mat = generate_mat_from_image(path)
    print(mat.shape)
    b_area_base = BArea(layers={'base_layer': BLayer(name='layer1', mat=mat)})
    app = QApplication(sys.argv)
    b_platform = BPlatform()
    b_platform.base_obj_init(BWindowWorker('Base Window 1'), mat, b_area_base,
                           b_area_worker=BAreaWorker('First', b_area_base), b_figure_worker=BFigureWorker('F1'))
    # b_platform.show_window('m1')
    # b_platform.ui_show_window()
    b_platform.show()
    sys.exit(app.exec_())
