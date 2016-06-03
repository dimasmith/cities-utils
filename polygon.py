class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self, *args, **kwargs):
        return 'Point{x=' + str(self.x) + ',y=' + str(self.y) + '}'

class Polygon:
    def __init__(self, points):
        self.points = points

    def find_inclusive_center(self):
        pass