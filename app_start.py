from base_objs.b_obj import BWindowWorker, BAreaWorker, BFigureWorker, BArea, BLayer
from base_objs.b_platform import BPlatform
from b_mat.b_mat_worker import generate_mat_from_image

if __name__ == '__main__':
    print('start!!!')
    path = '/home/kostegan/work2021/scripts/b_platform/resize_test_img.png'

    mat = generate_mat_from_image(path)
    print(mat.shape)
    print(mat[0][0])
    b_area_base = BArea(layers={'base_layer': BLayer(name='layer1', mat=mat)})
    b_platform = BPlatform(BWindowWorker('Base Window 1'), mat, b_area_base,
                           b_area_worker=BAreaWorker('First', b_area_base), b_figure_worker=BFigureWorker('F1'))
    b_platform.show_window('m1')
    print('end!!!')
