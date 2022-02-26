import unittest
import numpy as np
import cv2

from base_objs.b_obj import BCanvas

img_3 = np.zeros([512, 512, 4], dtype=np.uint8)
img_3.fill(255)

class TestNBPlatformBaseMethods(unittest.TestCase):


    def test_points(self):
        img_3 = np.zeros([512, 512, 4], dtype=np.uint8)
        img_3.fill(255)
        bc = BCanvas()
        bc.init_b_area_drawer(img_3)
        x1,y1 = (10,10)
        xb1, yb1 = (50, 30)
        x2,y2 = (200,300)
        xb2, yb2 = (400, 40)
        bc.add_points(x1,y1,2,(0,25,0))
        bc.add_points(x2,y2,2,(0,25,0))
        bc.add_points(xb1,yb1,2,(0,25,0))
        bc.add_points(xb2,yb2,2,(0,25,0))
        bc.add_line(x1, y1, xb1, yb1, (0, 25, 0),1)
        bc.add_line(x2, y2, xb2, yb2, (0, 25, 0),1)
        # img_3 = bc.add_curve(10,10,200,400,600,200,70,80)
        img_3 = bc.add_curve(x1,y1,50,30,400,40,x2,y2)
        cv2.imwrite('./ex2.png', img_3)
        print('final1')

if __name__ == '__main__':
    pass
    # unittest.main()
    # cv2.imwrite('./ex2.png', img_3)
    # print('final1')
