from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()


def on_press(key):
    try:
        if key.char == 'w':
            keyboard.tap(Key.f1)
    except AttributeError:
        pass


listener = Listener(on_press=on_press)
listener.start()
