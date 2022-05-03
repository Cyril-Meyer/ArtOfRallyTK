import win32api
from pynput.keyboard import Key, Controller


# AZERTY keyboard
keys = ['Z', 'Q', 'S', 'D']
# output
keyboard = Controller()


def get_keys():
    array_out = [0, 0, 0, 0]
    for k in range(len(keys)):
        if win32api.GetAsyncKeyState(ord(keys[k])):
            array_out[k] = 1
    return array_out


def set_keys(input):
    for k in range(len(input)):
        key = keys[k]
        if input[k] == 1:
            keyboard.press(key)
        else:
            keyboard.release(key)
    return
