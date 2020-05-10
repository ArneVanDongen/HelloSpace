
import time
from datetime import datetime

import krpc


def log_vessel_status():
    print('\tTelemetry')
    print('\t\t  direction: (%.2f, %.2f, %.2f)' % flight.direction)
    print('\t\t   velocity: (%.2f, %.2f, %.2f)' % flight.velocity)
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
            return 1
    elif flight_phase == 1:
        if flying_upwards():
            return 1
        else:
            return 2
    elif flight_phase == 2:
        if altitude() > 100 + LAUNCH_ALTITUDE:
            return 2
        else:
            control.gear = True
            return 3
    elif flight_phase == 3:
        if altitude() > 50 + LAUNCH_ALTITUDE:
            return 3
        else:
            return 4
    elif flight_phase == 4:
        if altitude() > LAUNCH_ALTITUDE:
            return 4
        else:
            return 5


def determine_throttle(throttle):
    """
    Determines based on true_air_speed and flight_phase what the throttle should be set to for the next second
    :param throttle: The current amount of throttle from 0 to 1
    :rtype: float
    :return: The new throttle value
    """
    print('\tdetermine_throttle: throttle={0}, altitude={1}, true_air_speed={2}, flying_upwards={3}'
          .format(round(throttle, 1), round(altitude(), 1), round(true_air_speed(), 1), flying_upwards()))
    max_throttle = 0.3
    fine_max_throttle = max_throttle / 1.5
    adjustment = 0.05
    small_adjustment = adjustment / 2
    fine_adjustment = adjustment / 8
    if flight_phase == 0:
        if true_air_speed() > 15:
            return throttle - adjustment
        else:
            new_throttle = throttle + adjustment
            return new_throttle if new_throttle <= max_throttle else throttle
    elif flight_phase == 1:
        return 0.1
    elif flight_phase == 2:
        if true_air_speed() > 7.5 and not flying_upwards():
            new_throttle = throttle + small_adjustment
            return new_throttle if new_throttle <= max_throttle else throttle
        else:
            return throttle - adjustment
    elif flight_phase == 3:
        if throttle > fine_max_throttle:
            return fine_max_throttle - small_adjustment
        elif true_air_speed() > 3.75 and not flying_upwards():
            new_throttle = throttle + small_adjustment
            return new_throttle if new_throttle <= fine_max_throttle else throttle
        else:
            return throttle - small_adjustment
    elif flight_phase == 4:
        if altitude() <= LAUNCH_ALTITUDE:
            return 0
        elif throttle > fine_max_throttle:
            return fine_max_throttle - fine_adjustment
        elif true_air_speed() > 1 and not flying_upwards():
            return throttle + fine_adjustment if throttle + fine_adjustment <= fine_max_throttle else throttle
        else:
            return throttle - fine_adjustment
    else:
        return 0


def flying_upwards():
    """
    if vertical velocity is positive
    :rtype: bool
    :return: Whether or not not the vessel is flying upwards
    """
    return prograde()[0] >= -0.05


# kRPC vars
connection = krpc.connect()
vessel = connection.space_center.active_vessel
flight = vessel.flight()
control = vessel.control

# Telemetry streams
altitude = connection.add_stream(getattr, vessel.flight(), 'mean_altitude')
g_force = connection.add_stream(getattr, vessel.flight(), 'g_force')
true_air_speed = connection.add_stream(getattr, vessel.flight(), 'true_air_speed')
prograde = connection.add_stream(getattr, vessel.flight(), 'prograde')

# Program vars
flight_phase = 0
LAUNCH_ALTITUDE = 80
TARGET_ALTITUDE = 250 + LAUNCH_ALTITUDE

print('\nSTARTING HOVER CONTROLLER')
start_time = datetime.utcnow()
print(start_time)
control.activate_next_stage()
control.throttle = 0.2

# The main loop
while flight_phase < 5:
    print('\n===========================================\n')
    print('{0} - T={1}'.format(datetime.utcnow(), round(vessel.met, 1)))

    flight_phase = update_flight_phase()
    print("\tcurrent flight_phase={0}".format(flight_phase))
    vessel.control.throttle = determine_throttle(vessel.control.throttle)
    print("\tcurrent throttle={0}".format(round(vessel.control.throttle, 2)))

    log_vessel_status()
    time.sleep(1)


print('\n===========================================\n')
print('ENDING HOVER CONTROLLER')
end_time = datetime.utcnow()
print(end_time)
print('Elapsed Mission Time: {0}'.format(end_time - start_time))
