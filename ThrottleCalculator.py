class ThrottleCalculator:

    def __init__(self, max_thrust):
        """
        :param float max_thrust: thrust with throttle at 1.0, in Newtons
        """
        self.max_thrust = max_thrust

    def calculate_needed_throttle(self, current_mass, speed_diff, time_to_impact, current_accel=9.81,
                                  current_accel_direction=-1):
        """
        Calculates the throttle needed for the desired speed change
        :param current_mass:
        :param speed_diff:
        :param current_accel:
        :param current_accel_direction:
        :return:
        """
        # TODO add time to impact
        current_force = current_mass * current_accel * current_accel_direction
        desired_accel = speed_diff / time_to_impact  # I want to get to that speed in 1 s
        accel_force = current_mass * desired_accel
        needed_force = accel_force + current_force
        print("\t\t/calculate_needed_thrust: current_mass={:.2f}, speed_diff={:.2f}, time_to_impact={:.2f}"
              .format(current_mass, speed_diff, time_to_impact))
        print("\t\t current_force={:.2f}, accel_force={:.2f}, needed_force={:.2f}"
              .format(current_force, accel_force, needed_force))
        print("\t\t\\return {:.2f}".format(needed_force / self.max_thrust))
        return needed_force / self.max_thrust

    def check_if_should_start_suicide_burn(self, current_mass, gravitational_accel, current_speed, time_to_impact):
        current_force = current_mass * gravitational_accel
        inertial_force = current_mass * (current_speed / time_to_impact)
        needed_force = inertial_force + current_force
        print("\t\t/check_if_should_start_suicide_burn: current_mass={:.2f}, gravitational_accel={:.2f}, "
              "current_speed={:.2f}, time_to_impact={:.2f}"
              .format(current_mass, gravitational_accel, current_speed, time_to_impact))
        print("\t\t needed_force = {:.2f}= (inertial_force={:.2f} + current_force={:.2f})"
              .format(needed_force, inertial_force, current_force))
        print("\t\t\\should start suicide burn? {:.0f} <= {:.0f} = {}"
              .format(self.max_thrust, needed_force, self.max_thrust <= needed_force))
        return self.max_thrust <= needed_force
