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
vessel.control.throttle = 0.3
objective_achieved = False
flight = vessel.flight()

# Streams for telemetry
ut = connection.add_stream(getattr, connection.space_center, 'ut')
altitude = connection.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = connection.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
stage_0_resources = vessel.resources_in_decouple_stage(stage=0, cumulative=False)
liquid_fuel_stage_0 = connection.add_stream(stage_0_resources.amount, 'LiquidFuel')
stage_1_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
liquid_fuel_stage_1 = connection.add_stream(stage_1_resources.amount, 'LiquidFuel')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
liquid_fuel_stage_2 = connection.add_stream(stage_2_resources.amount, 'LiquidFuel')
stage_3_resources = vessel.resources_in_decouple_stage(stage=3, cumulative=False)
liquid_fuel_stage_3 = connection.add_stream(stage_3_resources.amount, 'LiquidFuel')
stage_4_resources = vessel.resources_in_decouple_stage(stage=4, cumulative=False)
liquid_fuel_stage_4 = connection.add_stream(stage_4_resources.amount, 'LiquidFuel')

print('Start lon', flight.longitude)
print('Start lat', flight.latitude)
print('Start alt', flight.mean_altitude)


while not objective_achieved:
    print('\nT=', round(vessel.met, 1))

    print('ut?', ut())
    print('altitude', altitude())
    print('apoapsis', apoapsis())
    print('liquid_fuel_stage_0', liquid_fuel_stage_0())
    print('liquid_fuel_stage_1', liquid_fuel_stage_1())
    print('liquid_fuel_stage_2', liquid_fuel_stage_2())
    print('liquid_fuel_stage_3', liquid_fuel_stage_3())
    print('liquid_fuel_stage_4', liquid_fuel_stage_4())

    log_vessel_status()

    desired_unit_vector = calc_desired_unit_vector(flight.longitude, flight.mean_altitude)
    adjusted_direction = get_true_unit_vector(flight.direction)
    difference_vector = calculate_difference(desired_unit_vector, adjusted_direction)
    log_trajectory_status()

    time.sleep(1)

