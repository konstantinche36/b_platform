from b_layer.b_layer import BLayer


class BLayerBD:
    def __init__(self, name):
        self.name = name
        self.bd = {}

    def get_layers(self):
        return self.bd.values()

    def add_layer(self, layer_name, layer: BLayer):
        self.bd[layer_name] = layer

    def get_layer_by_name(self, layer_name) -> BLayer:
        return self.bd[layer_name]
