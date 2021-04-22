class BApp:
    def __init__(self, img_worker):
        self.img_worker = img_worker

    def start(self):
        self.img_worker.resize_image_mat(100)
        self.img_worker.configure_window_for_img()
        self.img_worker.create_figure('bezie01')
        # print(self.img_worker)
        self.img_worker.show_image()
        # self.img_worker.show_image()
