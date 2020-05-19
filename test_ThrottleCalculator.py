from unittest import TestCase
from ThrottleCalculator import ThrottleCalculator


class TestThrottleCalculator(TestCase):

    def test_calculate_needed_thrust(self):
        mass = 17_000
        max_thrust = 1_000_000
        speed_diff = 200
        calculator = ThrottleCalculator(max_thrust)
        calculated_throttle = calculator.calculate_needed_thrust(mass, speed_diff, 3)
        expected_calculated_throttle = 0.966563
        self.assertAlmostEqual(calculated_throttle, expected_calculated_throttle, 3)
