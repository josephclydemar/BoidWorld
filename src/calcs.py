import math


def calc_distance(position1, position2):
    return math.sqrt(math.pow(position1[0] - position2[0], 2) + math.pow(position1[1] - position2[1], 2))