import numpy
import cairo
import math

data = numpy.zeros((1000, 1000, 4), dtype=numpy.uint32)
surface = cairo.ImageSurface.create_for_data(
    data,
    cairo.FORMAT_ARGB32,
    1000, 1000)
cr = cairo.Context(surface)
ctx = cairo.Context(surface)

# Paint the background
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

lists = [[0, 250], [100, 50], [239, 390], [350, 150], [99, 200]]

# x, y, x1, y1 = 0, 250, 100, 50
# x2, y2, x3, y3 = 239, 390, 350, 150
x, y, x1, y1 = lists[0][0], lists[0][1], lists[1][0], lists[1][1]
x2, y2, x3, y3 = lists[2][0], lists[2][1], lists[3][0], lists[3][1]
# x4, y4 = 400, 10

# Draw the image
ctx.move_to(x, y)
ctx.curve_to(x1, y1, x2, y2, x3, y3)
ctx.curve_to(x3, y3, x3 + x2 * (-1) + x3, y3 + y2 * (-1) + y3, 99, 200)
ctx.set_source_rgb(1, 0, 0)
ctx.set_line_width(2)
ctx.stroke()


ctx.set_source_rgba(0, 0, 0, 0.7)
ctx.set_line_width(1.2)
ctx.move_to(x, y)
ctx.line_to(x1, y1)
ctx.move_to(x2, y2)
ctx.line_to(x3, y3)
ctx.move_to(x3, y3)
ctx.line_to(x3 + x2 * (-1) + x3, y3 + y2 * (-1) + y3)
ctx.stroke()

def add_point_to_sur(x, y, color):
    ctx.set_source_rgb(color[0], color[1], color[2])
    ctx.arc(x, y, 5, 0, 2 * math.pi)
    ctx.fill()
    ctx.fill_preserve()
    print('ok')


for i in lists:
    add_point_to_sur(i[0], i[1], (0, 255, 255))

ctx.stroke()
# print(data[100:150,100:150,0])
# Save the result
# typesurface.get_data()
surface.write_to_png('bezier.png')

# if __name__ == '__main__':
#     lists = [[0, 250], [100, 50], [239, 390], [350, 150]]
#     print(lists[0])
