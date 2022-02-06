import unittest

from b_mat.b_mat_worker import generate_mat_from_image
from base_objs.nb_platform import BPlatform
from base_objs.b_obj import BFigure, BPoint, BFigureWorker

m1 = BPlatform(generate_mat_from_image('../ui/pic1.jpg'))
point = BPoint('DemoPoint', 10, 10)
figure = BFigure('DemoFigure', [point])
m1.b_figure_worker.save_figure_to_bd(figure)


class TestNBPlatformBaseMethods(unittest.TestCase):

    def test_get_selected_figure(self):
        self.assertTrue(m1.selected_figure is None)

    def test_set_selected_figure(self):
        x, y = (10, 10)
        self.assertEqual(m1.simple_select(x, y), figure)
        self.assertEqual(m1.simple_select(x, y), point)



if __name__ == '__main__':
    unittest.main()
