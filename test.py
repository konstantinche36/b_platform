import cv2

def click_event(self, event, x, y, flags, params=None):
    # if event == cv2.EVENT_LBUTTONDOWN:
    print(x, y)

mat = cv2.imread('/home/kostegan/work2021/scripts/b_platform/resize_test_img.png')
cv2.imshow('ll', mat)
cv2.setMouseCallback('ll', click_event)
while True:
    key = cv2.waitKey()
    if key == 27:
        break
cv2.destroyAllWindows()


# def click_event(self, event, x, y, flags, params):
#     # if event == cv2.EVENT_LBUTTONDOWN:
#     print(x, y)

# pass
# if IS_EDIT_MODE:
#     global bx1, by1, bx2, by2, cur_x, cur_y, first_x, first_y, second_x, second_y, l2
#     if event == cv2.EVENT_LBUTTONDOWN:
#         first_x, first_y = x, y
#         self.img_mat = self.b_figures.get('bezie01').insert_point(x, y, self.img_mat)
#         l2 = self.img_mat
#     if event == cv2.EVENT_MOUSEMOVE:
#         self.img_mat = self.b_figures.get('bezie01').show_points(x, y, self.img_mat)
