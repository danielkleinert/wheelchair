from pynput.keyboard import Key, Controller, Listener
from data_types import Game


def listen_for_restart(game: Game):
    keyboard = Controller()

    def on_press(key):
        try:
            if key.char == 'w':
                keyboard.tap(Key.f1 if game == Game.MARIO_KART_WII else Key.f7)
        except AttributeError:
            pass

    listener = Listener(on_press=on_press)
    listener.start()
