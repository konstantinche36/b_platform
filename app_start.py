from base_objs import b_obj, b_platform
if __name__ == '__main__':
    path = 'resize_test_img.png'
    mat = b_obj.generate_mat_from_image(path)
    mats = b_obj.BMatBD([mat])
    b_platform = b_platform.BPlatform(b_obj.BWindowShower(),mats)
    b_platform.show()
