from pymongo import MongoClient
from polygon import Point
from math import floor

client = MongoClient()
db = client['giz2']
districts_collection = db['districts']
districts = districts_collection.find()
aug_districts = db['districts_aug']

polygon = '<polygon points="812,352 813,352 814,352 815,353 816,352 817,353 818,352 818,351 819,352 820,352 821,352 822,353 823,353 824,354 824,355 825,356 826,357 827,357 828,358 829,358 830,359 829,360 828,360 827,361 826,362 826,363 827,364 827,365 827,366 826,366 825,366 824,367 824,368 823,368 822,368 821,367 820,367 819,367 818,367 817,367 816,367 815,367 814,366 814,365 813,364 814,363 814,362 814,361 814,360 814,359 815,358 815,357 814,356 814,355 813,354 812,353"/>'


def find_inclusive_center(points):
    min_y = min(points, key=lambda p: p.y).y
    max_y = max(points, key=lambda p: p.y).y
    height_median = max_y - floor((max_y - min_y) / 2)
    points_on_median = list(filter(lambda p: p.y == height_median, points))
    x_on_median = list(sorted([p.x for p in points_on_median]))

    x0 = x_on_median[0]
    x1 = x_on_median[len(x_on_median ) - 1]

    horizontal_median = x1 - (floor((x1 - x0) / 2))

    return Point(int(horizontal_median), int(height_median))


def convert_tuple_to_point(tuple_str):
    x, y = tuple_str.split(',')
    return Point(int(x), int(y))


def extract_points(polygon_str):
    points_str = polygon_str.replace('<polygon points="', '').replace('"/>', '')
    if points_str == '':
        return []
    points_str_tuples = points_str.split(' ')
    return list(map(convert_tuple_to_point, points_str_tuples))


for d in districts:
    polygon = d['polygon']
    points = extract_points(polygon)
    if len(points) == 0:
        print(d)
        continue
    center = find_inclusive_center(points)
    d['center'] = {'x': center.x, 'y': center.y}
    districts_collection.save(d)
