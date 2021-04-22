class BItem:
    def __init__(self):
        self.items = []

    def add_point(self, b_point):
        self.items.append(b_point)

    def get_str_of_points(self):
        result = ''
        for i, e in enumerate(self.items):
            result += f'\t- point_{i+1} x = {e.x} y = {e.y}\n'
        return result

    def __str__(self):
        return f'... B\nObject of a class <BItem>\npoints[\n{self.get_str_of_points()}]\n...'


class BPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'... B\nObject of a class <BPoint>\nx = {self.x}, y = {self.y}\n...'


if __name__ == '__main__':
    point1 = BPoint(25, 14)
    point2 = BPoint(25, 14)
    b_item = BItem()
    b_item.add_point(point1)
    b_item.add_point(point2)
    # print(b_item.get_str_of_points())
    print(b_item)
    # b_item.add_point(point1)
    # b_item.add_point(point2)
    # print(b_item)
