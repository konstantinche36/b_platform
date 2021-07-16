class BLayer:
    def __init__(self, name, mat):
        self.name = name
        self.mat = mat

    def get_layer_name(self):
        return self.name

    def get_layer_mat(self):
        return self.mat

    def set_layer_mat(self, mat):
        self.mat = mat

