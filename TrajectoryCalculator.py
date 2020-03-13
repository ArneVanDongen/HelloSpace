import math
from VectorUtils import *
from Transformers import *


starting_longitude = -74.55769195879196
starting_altitude = 84.32061045709997
starting_latitude = -0.09715892195951778


def set_starting_longitude(longitude):
    global starting_longitude
    starting_longitude = longitude


def translate_longitude_to_m(actual_longitude):
    return longitude_diff_to_meters(starting_longitude, actual_longitude, starting_latitude)


def translate_altitude(actual_altitude):
    return starting_altitude-actual_altitude


def get_altitude(longitude):
    log_operation('altitude', 'longitude', longitude)
    return 200 * math.sqrt(5 / 3) * math.sqrt(translate_longitude_to_m(longitude))


def get_longitude(altitude):
    log_operation('longitude', 'altitude', altitude)
    return (altitude / (200 * math.sqrt(5 / 3))) ** 2


def log_operation(goal, label, value):
    print('\t\tTrajectory', goal, 'at', label, 'should be', round(value, 1))


# Adjustment vectors

def calc_desired_vector(actual_longitude, actual_altitude):
    longitude_distance = translate_longitude_to_m(actual_longitude)
    altitude = actual_altitude
    desired_altd_1 = get_altitude(longitude_distance)
    desired_long_1 = get_longitude(altitude)
    desired_altd_2 = get_altitude(longitude_distance + 20)
    desired_long_2 = get_longitude(desired_altd_2)
    desired_vector = calculate_vector_from_xy(desired_long_1, desired_altd_1, desired_long_2, desired_altd_2)
    print('\t\t\t desired vector: (%.3f, %.3f, %.3f)' % desired_vector)
    return desired_vector


def calc_desired_unit_vector(actual_longitude, actual_altitude):
    desired_vector = calc_desired_vector(actual_longitude, actual_altitude)
    max_value = max(desired_vector)
    desired_unit_vector = desired_vector[0] / max_value, desired_vector[1] / max_value, desired_vector[2] / max_value
    print('\t\t\t desired unit vector: (%.3f, %.3f, %.3f)' % desired_unit_vector)
    return desired_unit_vector
