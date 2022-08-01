import win32api


def check_key(k):
    if win32api.GetAsyncKeyState(k):
        return True
    return False


def get_keys():
    # AZERTY
    keys = ['Z', 'Q', 'S', 'D']
    array_out = [0, 0, 0, 0]
    for k in range(len(keys)):
        if win32api.GetAsyncKeyState(ord(keys[k])):
            array_out[k] = 1
    return array_out
