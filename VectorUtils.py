def calculate_vector_from_xy(x1, y1, x2, y2):
    print('\t\t\tcalculating vector from point a =', round(x1, 2), round(y1, 2), 'to point b =', round(x2, 2), round(y2, 2))
    return (x2-x1), 0, (y2-y1)


def calculate_difference(desired_vector, actual_vector):
    return desired_vector[0] - actual_vector[0], \
           desired_vector[1] - actual_vector[1], \
           desired_vector[2] - actual_vector[2]
