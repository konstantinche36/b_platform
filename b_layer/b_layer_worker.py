from b_layer.b_layer_bd import BLayerBD
from b_layer.b_layer import BLayer


class BLayerWorker:

    def __init__(self):
        self.bd = BLayerBD('default_bd')

    def create_layer(self, name, mat):
        self.bd.add_layer(name, BLayer(name, mat))

    def get_mat_by_layer_name(self, name):
        return self.bd.get_layer_by_name(name).get_layer_mat()
