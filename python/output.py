from datetime import datetime, timedelta
import math
from pynput.keyboard import Controller
from data_types import Steering
import asyncio

SAMPLING_RATE = 30
FORWARD_EVERY_X_TICKS = 1000
MAX_FORWARD_BUTTON_EVERY_SECS = 0.4
ROTATION_PRESS_TIME = (1 / SAMPLING_RATE) * 1.0


class KeyboardOutput:
    """ modulate forward/backward as times w/s pressed and left right as key-down time of a/d
        for https://store.steampowered.com/app/871510/Wheelchair_Simulator/ """

    def __init__(self) -> None:
        self.keyboard = Controller()
        self.forward = 0
        self.lastForwardTime = datetime.now()
        self.release_times = {
            'a': None,
            'd': None,
        }
        for key in ['d', 'a']:
            asyncio.create_task(self.check_key_up(key))

    def send_control(self, steering: Steering):
        self.forward += steering.forward
        forward = abs(self.forward) > FORWARD_EVERY_X_TICKS
        self.forward %= math.copysign(FORWARD_EVERY_X_TICKS, self.forward)

        if forward and self.lastForwardTime + timedelta(seconds=MAX_FORWARD_BUTTON_EVERY_SECS) < datetime.now():
            self.lastForwardTime = datetime.now()
            if self.forward > 0:
                self.keyboard.tap('w')
            if self.forward < 0:
                self.keyboard.tap('s')
        if steering.right > 0:
            self.press('d', steering.right)
        if steering.right < 0:
            self.press('a', -steering.right)

    @staticmethod
    def get_forward_taps_and_rest(ticks, every=FORWARD_EVERY_X_TICKS):
        a = divmod(ticks, int(math.copysign(every, ticks)))
        return a

    def press(self, key: str, intensity: float):
        delta = timedelta(milliseconds=ROTATION_PRESS_TIME * intensity)
        if self.release_times[key] is None:
            self.keyboard.press(key)
        self.release_times[key] = datetime.now() + delta

    async def check_key_up(self, key):
        while True:
            release_time = self.release_times[key]
            if release_time is None:
                await asyncio.sleep(1/120)
                continue
            wait_time = release_time - datetime.now()
            if wait_time < timedelta(milliseconds=0):
                self.keyboard.release(key)
                self.release_times[key] = None
            else:
                await asyncio.sleep(wait_time.total_seconds())
