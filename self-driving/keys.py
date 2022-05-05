import win32api, win32con
import pyautogui
pyautogui.FAILSAFE = False

# AZERTY keyboard
keys = ['Z', 'Q', 'S', 'D']


def get_keys():
    array_out = [0, 0, 0, 0]
    for k in range(len(keys)):
        if win32api.GetAsyncKeyState(ord(keys[k])):
            array_out[k] = 1
    return array_out


def set_keys(input):
    print(input)
    for k in range(len(input)):
        key = keys[k]
        if input[k] == 1 and set_keys_static_input_1[k] == 0:
            print('keyDown', key)
            pyautogui.keyDown(key)
            set_keys_static_input_1[k] = 1
        elif input[k] == 0 and set_keys_static_input_1[k] == 1:
            print('keyUp', key)
            pyautogui.keyUp(key)
            set_keys_static_input_1[k] = 0
    return
set_keys_static_input_1 = [0, 0, 0, 0]


def check_quit_key():
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        return True
    return False
