from datetime import datetime, timedelta
from pynput.keyboard import Key, Controller
from data_types import Steering, Game
import asyncio
try:
    from blessings import Terminal
    term = Terminal()
except:
    term = None

SAMPLING_RATE = 30
DEADZONE = 10


class KeyboardOutput:

    def __init__(self, game: Game) -> None:
        if term:
            print(term.clear)
        self.rotation_press_time = (1 / SAMPLING_RATE) * 1.5 if game == Game.MARIO_KART_WII else 0.8
        self.forward_press_time = (1 / SAMPLING_RATE) * 10 if game == Game.MARIO_KART_WII else 0.9
        self.keyboard = Controller()
        self.release_times = {}
        asyncio.create_task(self.check_key_up())

    def send_control(self, steering: Steering):
        if term:
            print(term.normal, term.move(0, 0), term.clear_eol, steering.forward, term.move(0, 8), steering.right)
        if steering.forward > DEADZONE:
            self.press('u', steering.forward * self.forward_press_time)
        if steering.forward < -DEADZONE:
            self.press('i', -steering.forward * self.forward_press_time)
        if steering.right > DEADZONE:
            self.press(Key.right, steering.right * self.rotation_press_time)
        if steering.right < -DEADZONE:
            self.press(Key.left, -steering.right * self.rotation_press_time)

    def press(self, key: str, time: float):
        delta = timedelta(milliseconds=time)
        if self.release_times.get(key, None) is None:
            self.keyboard.press(key)
        self.release_times[key] = datetime.now() + delta

    async def check_key_up(self):
        while True:
            if term:
                print(term.move(0, 1))
            for key in self.release_times.keys():
                release_time = self.release_times[key]
                if release_time is not None and release_time < datetime.now():
                    self.keyboard.release(key)
                    self.release_times[key] = None
                if term:
                    print((term.on_blue if release_time else "") + f" {key} " + term.normal)
            await asyncio.sleep(1 / 60)
