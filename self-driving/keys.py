import win32api

# AZERTY keyboard
keys = ['Z', 'Q', 'S', 'D']


def get_keys():
    array_out = [0, 0, 0, 0]
    for k in range(len(keys)):
        if win32api.GetAsyncKeyState(ord(keys[k])):
            array_out[k] = 1
    return array_out
