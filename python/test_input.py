from unittest import TestCase
from data_types import Steering, WheelRotation
from input import map_to_steering

cases = [
    (WheelRotation(0, 0), Steering(0, 0)),
    (WheelRotation(100, 105), Steering(100, -5)),
    (WheelRotation(-100, -105), Steering(-100, 5)),
    (WheelRotation(10, -10), Steering(0, 20)),
    (WheelRotation(-10, 1), Steering(0, -11)),
]


class Test(TestCase):
    def test_map_to_steering(self):
        for wheel_rotation, steering in cases:
            with self.subTest(str(wheel_rotation) + " => " + str(steering)):
                self.assertEqual(map_to_steering(wheel_rotation), steering)
