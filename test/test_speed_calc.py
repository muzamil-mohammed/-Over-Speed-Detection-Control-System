"""
test_speed_calc.py
--------------------
Automated unit tests for the speed-calculation logic mirrored from
the Arduino firmware (see src/speed_utils.h and src/over_speed_detection.ino).

Run with:
    python -m unittest test/test_speed_calc.py -v
"""

import unittest
from speed_calc_simulation import calculate_speed_kmph, evaluate_speed, SPEED_LIMIT_KMPH


class TestSpeedCalculation(unittest.TestCase):

    def test_known_speed_value(self):
        # 0.20 m in 0.10 s -> 2 m/s -> 7.2 km/h
        speed = calculate_speed_kmph(0.20, 0.10)
        self.assertAlmostEqual(speed, 7.2, places=2)

    def test_zero_time_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_speed_kmph(0.20, 0)

    def test_negative_time_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_speed_kmph(0.20, -0.05)

    def test_slow_speed_is_normal(self):
        speed = calculate_speed_kmph(0.20, 0.30)  # 2.4 km/h
        self.assertLess(speed, SPEED_LIMIT_KMPH)
        self.assertIn("Normal", evaluate_speed(speed))

    def test_fast_speed_triggers_alert(self):
        speed = calculate_speed_kmph(0.20, 0.08)  # 9.0 km/h
        self.assertGreater(speed, SPEED_LIMIT_KMPH)
        self.assertIn("OVER SPEED", evaluate_speed(speed))

    def test_boundary_speed_at_limit(self):
        # Exactly at the limit should NOT be flagged as over-speed
        result = evaluate_speed(SPEED_LIMIT_KMPH, limit_kmph=SPEED_LIMIT_KMPH)
        self.assertIn("Normal", result)


if __name__ == "__main__":
    unittest.main()
