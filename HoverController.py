import time
from datetime import datetime

import krpc

from ThrottleCalculator import ThrottleCalculator


def log_vessel_status():
    print('\tTelemetry')
    print('\t\t  direction: (%.2f, %.2f, %.2f)' % flight.direction)
    print('\t\t       drag: (%.2f, %.2f, %.2f)' % flight.drag)
    print('\t\t   prograde: (%.2f, %.2f, %.2f)' % prograde())
    print('\t\t   altitude: %.2f' % altitude())
    print('\t\t  air_speed: %.2f' % true_air_speed())
    print('\t\t    g_force: %.2f' % g_force())
    print('\t\t   throttle: %.2f' % vessel.control.throttle)
    print('\t\t      phase: %.0f' % flight_phase)


def update_flight_phase():
    """
    :return:
        indicating this flight's phase (0=ascending, 1=stop_ascend, 2=descending, 3=slow_descend, 4=landing, 5=landed)
    :rtype: int
    """
    print('\tupdate_flight_phase: flight_phase={0}, altitude={1}, true_air_speed={2}'
          .format(round(flight_phase, 0), round(altitude(), 2), round(true_air_speed(), 2)))
    if flight_phase == 0:
        control.gear = False
        if altitude() < TARGET_ALTITUDE:
            return 0
        else:
            control.gear = True
            return 1
    elif flight_phase == 1:
        if flying_upwards():
            return 1
        else:
            return 2
    elif flight_phase == 2:
        # TODO find center of mass height instead of magic number
        if altitude() > 7.6:
            return 2
        else:
            return 3


def determine_throttle(throttle):
    """
    Determines based on true_air_speed and flight_phase what the throttle should be set to for the next second
    :param float throttle: The current amount of throttle from 0 to 1
    :rtype: float
    :return: The new throttle value
    """
    print('\tdetermine_throttle: throttle={0}, altitude={1}, true_air_speed={2}, flying_upwards={3}'
          .format(round(throttle, 1), round(altitude(), 1), round(true_air_speed(), 1), flying_upwards()))
    direction = 1 if flying_upwards() else -1
    if flight_phase == 0:
        speed_diff = TARGET_SPEED - true_air_speed()
        return throttle_calculator.calculate_needed_throttle(vessel.mass, speed_diff,
                                                             2, flight.drag[0], kerbin.surface_gravity,
                                                             direction)
    else:
        burn = throttle_calculator.should_start_suicide_burn(vessel.mass, kerbin.surface_gravity, 0, true_air_speed(),
                                                             calculate_time_to_impact())
        if burn and not flying_upwards():
            return throttle_calculator.calculate_needed_throttle(vessel.mass, true_air_speed(),
                                                                 calculate_time_to_impact(), 0, 9.81,
                                                                 direction)
            # connection.space_center.target_body.surface_gravity()
        else:
            return 0


def calculate_time_to_target_altitude():
    return (TARGET_ALTITUDE - (altitude() - center_of_mass_height)) / true_air_speed()


def calculate_time_to_impact():
    return (altitude() - center_of_mass_height) / true_air_speed()


def calculate_suicide_burn_time(gravitational_accel, current_speed):
    time_to_suicide = current_speed / gravitational_accel
    print("\t\t calculate_suicide_burn_time: gravitational_accel={:.2f}, current_speed={:.2f}"
          .format(gravitational_accel, current_speed))
    print("\t\t return {:.2f}".format(time_to_suicide))
    return time_to_suicide


def flying_upwards():
    """
    if vertical velocity is positive
    :rtype: bool
    :return: Whether or not not the vessel is flying upwards
    """
    return prograde()[0] >= -0.05


# kRPC vars
connection = krpc.connect()
space_center = connection.space_center
vessel = space_center.active_vessel
bodies = space_center.bodies
kerbin = bodies['Kerbin']
flight = vessel.flight()
control = vessel.control
center_of_mass_height = 7.6

# Telemetry streams
altitude = connection.add_stream(getattr, vessel.flight(), 'surface_altitude')
g_force = connection.add_stream(getattr, vessel.flight(), 'g_force')
true_air_speed = connection.add_stream(getattr, vessel.flight(), 'true_air_speed')
prograde = connection.add_stream(getattr, vessel.flight(), 'prograde')

# Program vars
flight_phase = 0
TARGET_ALTITUDE = 500
TARGET_SPEED = 25

# region Start up sequence
print('\nSTARTING HOVER CONTROLLER')
print('Planning to hop to {}m, with a vertical speed of {} m/s'
      .format(TARGET_ALTITUDE, TARGET_SPEED))
start_time = datetime.utcnow()
print(start_time)
control.activate_next_stage()
throttle_calculator = ThrottleCalculator(vessel.max_thrust)
loop_separator = '\n===========================================\n'
# endregion

# region Main Controller Loop
while flight_phase < 3:
    print('%s' % loop_separator)
    print('{0} - T={1}'.format(datetime.utcnow(), round(vessel.met, 1)))

    flight_phase = update_flight_phase()
    print("\tcurrent flight_phase={0}".format(flight_phase))
    vessel.control.throttle = determine_throttle(vessel.control.throttle)
    print("\tcurrent throttle={0}".format(round(vessel.control.throttle, 2)))

    log_vessel_status()
    time.sleep(1 if flight_phase < 2 else 0.05)
# endregion

# region Shut down sequence
print(loop_separator)
print('ENDING HOVER CONTROLLER')
end_time = datetime.utcnow()
print(end_time)
print('Elapsed Mission Time: {0}'.format(end_time - start_time))
control.throttle = 0
# endregion
