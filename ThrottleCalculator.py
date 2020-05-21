class ThrottleCalculator:

    def __init__(self, max_thrust):
        """
        :param float max_thrust: thrust with throttle at 1.0, in Newtons
        """
        self.max_thrust = max_thrust

    def calculate_needed_throttle(self, current_mass, speed_diff, time_to_impact, drag, current_accel=9.81,
                                  current_accel_direction=-1):
        """
        Calculates the throttle needed for the desired speed change
        :param float current_mass: The current mass of the vessel in kg
        :param float speed_diff: The difference in speed that we want to achieve in m/s
        :param float current_accel: The current acceleration of the vessel, usually due to gravity in m/s^2
        :param int current_accel_direction: The direction of this acceleration, usually negative, in a signed number
        :rtype: float
        :return: a value from 0 to 1.00 denoting what the throttle should be set to
        """
        current_force = (current_mass * current_accel * current_accel_direction) + drag
        desired_accel = speed_diff / time_to_impact  # I want to get to that speed in 1 s
        accel_force = current_mass * desired_accel
        needed_force = accel_force + current_force
        print("\t\t/calculate_needed_thrust: current_mass={:.2f}, speed_diff={:.2f}, time_to_impact={:.2f}, drag={:.2f}"
              .format(current_mass, speed_diff, time_to_impact, drag))
        print("\t\t current_force={:.2f}, accel_force={:.2f}, needed_force={:.2f}"
              .format(current_force, accel_force, needed_force))
        print("\t\t\\return {:.2f}".format(needed_force / self.max_thrust))
        return needed_force / self.max_thrust

    def should_start_suicide_burn(self, current_mass, gravitational_accel, drag, current_speed, time_to_impact):
        """
        Checks if the suicide burn should start or not. By comparing the negative force of gravity and inertia,
        to the positive forces of drag and maximum engine thrust, we can see if there is still time to do a propulsive
        landing.
        :param float current_mass: The current mass of the vessel in kg
        :param float gravitational_accel: The gravitational acceleration in m/s^2
        :param float drag: The amount of drag on the y-axis in Newtons
        :param float current_speed: The current air speed in m/s
        :param float time_to_impact: The time it would take for us to reach the ground in s
        :rtype: bool
        :return: Whether or not the suicide burn should start
        """
        current_force = current_mass * gravitational_accel
        inertial_force = current_mass * (current_speed / time_to_impact)
        needed_force = inertial_force + current_force - drag
        print("\t\t/check_if_should_start_suicide_burn: current_mass={:.2f}, gravitational_accel={:.2f}, "
              "current_speed={:.2f}, time_to_impact={:.2f}"
              .format(current_mass, gravitational_accel, current_speed, time_to_impact))
        print("\t\t needed_force = {:.2f}= (inertial_force={:.2f} + current_force={:.2f} - drag={:.2f})"
              .format(needed_force, inertial_force, current_force, drag))
        print("\t\t\\should start suicide burn? {:.0f} <= {:.0f} = {}"
              .format(self.max_thrust, needed_force, self.max_thrust <= needed_force * 1.005))
        return self.max_thrust <= needed_force * 1.005
