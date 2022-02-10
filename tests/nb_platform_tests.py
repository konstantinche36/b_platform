import unittest
import numpy as np
from b_mat.b_mat_worker import generate_mat_from_image
from base_objs.nb_platform import BPlatform
from base_objs.b_obj import BFigure, BPoint, BFigureWorker
import cv2

img_3 = np.zeros([512,512,4],dtype=np.uint8)
img_3.fill(255)

# bpl = BPlatform(generate_mat_from_image('../ui/pic1.jpg'))
bpl = BPlatform(img_3)
point = BPoint('DemoPoint', 10, 10)
figure = BFigure('DemoFigure', [point])
bpl.b_figure_worker.save_figure_to_bd(figure)



class TestNBPlatformBaseMethods(unittest.TestCase):

    # def test_get_selected_figure(self):
    #     self.assertTrue(bpl.selected_figure is None)

    def test_add_point(self):
        x1, y1 = (10, 10)
        x2, y2 = (100, 100)
        x3, y3 = (25, 100)
        bpl.add_point(x1,y1)
        bpl.add_point(x2,y2)
        bpl.add_point(x3, y3)
        print(bpl.update_mat().shape)
        print(bpl.update_mat()[10][10])
        cv2.imwrite('./ex.png', bpl.update_mat())
        print('final1')




if __name__ == '__main__':
    unittest.main()
    cv2.imwrite('./ex.png', bpl.result_f_mat)
    print('final1')
