from base_objs.b_obj import generate_mat_from_image, BWindowWorker, BAreaWorker, BFigureWorker, BArea, BLayer
from base_objs.b_platform import BPlatform

if __name__ == '__main__':
    print('start!!!')
    path = '/home/kostegan/work2021/scripts/b_platform/resize_test_img.png'

    mat = generate_mat_from_image(path)
    print(mat.shape)
    print(mat[0][0])
    b_platform = BPlatform(BWindowWorker('Base Window 1'), BArea(layers=[BLayer(name='layer1', mat=mat)]),
                           b_area_worker=BAreaWorker('First'), b_figure_worker=BFigureWorker('F1'))
    b_platform.show_window('m1')
    print('end!!!')
