from base_objs.b_obj import generate_mat_from_image, BWindowWorker, BArea, BLayer
from base_objs.b_platform import BPlatform

if __name__ == '__main__':
    path = 'resize_test_img.png'
    mat = generate_mat_from_image(path)
    print(mat.shape)
    b_platform = BPlatform(BWindowWorker('Base Window 1'), BArea(layers=[BLayer(name='layer1', mat=mat)]),
                           b_area_worker=None)
    # b_platform.show()
