from base_objs import b_obj
if __name__ == '__main__':
    path = 'resize_test_img.png'
    window_shower = b_obj.BWindowShower(b_obj.generate_mat_from_image(path))
    window_shower.show_window()
