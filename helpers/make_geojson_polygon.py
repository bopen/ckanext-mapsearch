import random


def make_polygon_string():
    a = random.random() * 9 + 6
    b = random.random() * 13 + 35
    x_extent = random.random() * 3
    y_extent = random.random() * 3
    l = [[[a, b], [a + x_extent, b], [a + x_extent, b + y_extent],
          [a, b + y_extent], [a, b]]]
    return '{{"type":"Polygon","coordinates": {0}}}'.format(l)

if __name__ == '__main__':
    print make_polygon_string()
