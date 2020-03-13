import krpc
import time
from TrajectoryCalculator import *


def log_vessel_status():
    print('Telemetry')
    print('\t  direction/orientation:  (%.2f, %.2f, %.2f)' % flight.direction)
    print('\t     center of mass pos:  (%.2f, %.2f, %.2f)' % flight.center_of_mass)
    print('\t               velocity:  (%.3f, %.3f, %.3f)' % flight.velocity)
    print('\t               rotation:  (%.1f, %.1f, %.1f, %.1f)' % flight.rotation)
    print('\t      aerodynamic force:  (%.1f, %.1f, %.1f)' % flight.aerodynamic_force)
    print('\t                   lift:  (%.3f, %.3f, %.3f)' % flight.lift)
    print('\t                   drag:  (%.1f, %.1f, %.1f)' % flight.drag)


def log_trajectory_status():
    print('Trajectory')
    print('\t       adjusted current:  (%.3f, %.3f, %.3f)' % adjusted_direction)
    print('\t      difference_vector:  (%.3f, %.3f, %.3f)' % difference_vector)


connection = krpc.connect()
vessel = connection.space_center.active_vessel
vessel.control.throttle = 1
objective_achieved = False
flight = vessel.flight()

print('Start lon', flight.longitude)
print('Start lat', flight.latitude)
print('Start alt', flight.mean_altitude)


while not objective_achieved:
    print('\nT=', round(vessel.met, 1))
    log_vessel_status()

    desired_unit_vector = calc_desired_unit_vector(flight.longitude, flight.mean_altitude)
    adjusted_direction = get_true_unit_vector(flight.direction)
    difference_vector = calculate_difference(desired_unit_vector, adjusted_direction)
    log_trajectory_status()

    time.sleep(1)

