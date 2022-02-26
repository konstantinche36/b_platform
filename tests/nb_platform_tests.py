import unittest
import numpy as np
from b_mat.b_mat_worker import generate_mat_from_image
from base_objs.nb_platform import BPlatform
from base_objs.b_obj import BFigure, BPoint, BFigureWorker, BAreaDrawer, BAreaWorker
import cv2

img_3 = np.zeros([512, 512, 4], dtype=np.uint8)
img_3.fill(255)

# bpl = BPlatform(generate_mat_from_image('../ui/pic1.jpg'))
bpl:BPlatform = BPlatform(img_3)
# point = BPoint('DemoPoint', 10, 10)
figure = BFigure('DemoFigure', None)
bpl.b_figure_worker.save_figure_to_bd(figure)


class TestNBPlatformBaseMethods(unittest.TestCase):

    # def test_get_selected_figure(self):
    #     self.assertTrue(bpl.selected_figure is None)

    # def test_add_point(self):
    #     x1, y1 = (10, 10)
    #     x2, y2 = (100, 100)
    #     x3, y3 = (25, 100)
    #     bpl.add_point(x1, y1)
    #     bpl.add_point(x2, y2)
    #     bpl.add_point(x3, y3)
    #     # print(bpl.redraw_mat().shape)
    #     # print(bpl.redraw_mat()[10][10])
    #     bpl.redraw_mat()
    #     cv2.imwrite('./ex.png', bpl.result_f_mat)
    #     print('final1')
    #
    def test_add_point2(self):
        x1, y1 = (50, 10)
        x2, y2 = (100, 60)
        x3, y3 = (200, 10)
        x4, y4 = (300, 60)
        bpl.add_point(x1, y1)
        bpl.add_point(x2, y2)
        bpl.add_point(x3, y3)
        bpl.add_point(x4, y4)
        bpl.select(x2, y2)
        bpl.edit_point(55, 50)
        bpl.redraw_mat()
        cv2.imwrite('./ex.png', bpl.result_f_mat)
        print('final1')


if __name__ == '__main__':
    unittest.main()
    cv2.imwrite('./ex.png', bpl.result_f_mat)
    print('final1')
