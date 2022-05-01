from pynput.keyboard import Controller
from data_types import Steering

FORWARD_FACTOR = 1
ROTATION_FACTOR = 1

keyboard = Controller()


def send_control(steering: Steering):
    if steering.forward > 0:
        press('w', steering.forward * FORWARD_FACTOR)
    if steering.forward < 0:
        press('s', -steering.forward * FORWARD_FACTOR)
    if steering.right > 0:
        press('d', steering.right * ROTATION_FACTOR)
    if steering.right < 0:
        press('a', -steering.right * ROTATION_FACTOR)


def press(key: str, intensity: float):
    for x in range(int(intensity)):
        keyboard.press(key)
        keyboard.release(key)

