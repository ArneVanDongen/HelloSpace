from unittest import TestCase
from ThrottleCalculator import ThrottleCalculator


class TestThrottleCalculator(TestCase):

    def test_calculate_needed_throttle(self):
        mass = 17_000
        max_thrust = 1_000_000
        speed_diff = 200
        calculator = ThrottleCalculator(max_thrust)
        calculated_throttle = calculator.calculate_needed_throttle(mass, speed_diff, 3, 0)
        expected_calculated_throttle = 0.966563
        self.assertAlmostEqual(calculated_throttle, expected_calculated_throttle, 3)

    def test_calculate_needed_throttle_with_drag(self):
        mass = 17_000
        max_thrust = 1_000_000
        speed_diff = 200
        drag = 4000
        calculator = ThrottleCalculator(max_thrust)
        calculated_throttle = calculator.calculate_needed_throttle(mass, speed_diff, 3, drag)
        expected_calculated_throttle = 0.970563
        self.assertAlmostEqual(calculated_throttle, expected_calculated_throttle, 3)

    def test_should_start_suicide_burn(self):
        max_thrust = 937_321
        mass = 19171.49
        gravity = 9.81
        drag = 7169.57
        speed = 84.23
        time_to_impact = 2.08
        calculator = ThrottleCalculator(max_thrust)
        self.assertTrue(calculator.should_start_suicide_burn(mass, gravity, drag, speed, time_to_impact))

    def test_should_not_start_suicide_burn(self):
        max_thrust = 937_321
        mass = 19244.93
        gravity = 9.81
        drag = 7047.71
        speed = 84.12
        time_to_impact = 2.16
        calculator = ThrottleCalculator(max_thrust)
        self.assertFalse(calculator.should_start_suicide_burn(mass, gravity, drag, speed, time_to_impact))
