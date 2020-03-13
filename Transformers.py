import math


radius_m = 600_000
circumference_m = 3_769_911


def latitude_diff_to_m(lat1, lat2):
    lat_unit = (circumference_m / 360)
    return math.fabs(lat1 - lat2) * lat_unit


def longitude_diff_to_meters(lon1, lon2, lat):
    lon_unit = circumference_m * math.cos(lat) / 360
    return math.fabs(lon1 - lon2) * lon_unit


def haversine(lat1, lon1, lat2, lon2):
    d_lat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    d_lon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * \
        math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius_m / 1000 * c
    return d * 1000


def vector_to_controls(adjustment_vector):
    pass


def get_true_unit_vector(vector):
    biggest_value = 0
    for value in vector:
        if math.fabs(value) > biggest_value:
            biggest_value = value

    return vector[0] / biggest_value, vector[1] / biggest_value, vector[2] / biggest_value
