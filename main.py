from b_app.b_app import BApp
from b_img.b_img import BImageWorker, BImage

if __name__ == '__main__':
    image_worker = BImageWorker(BImage('test_img.png'))
    app = BApp(image_worker)
    app.start()
