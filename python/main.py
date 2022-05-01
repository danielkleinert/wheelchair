from input import map_to_steering
from output import send_control
from data_types import WheelRotation

if __name__ == '__main__':
    send_control(map_to_steering(WheelRotation(3, 4)))
