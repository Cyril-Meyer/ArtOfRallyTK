import numpy as np
import win32gui


def move_window_0(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    rect = win32gui.GetWindowRect(hwnd)
    xsize, ysize = rect[2] - rect[0], rect[3] - rect[1]
    win32gui.MoveWindow(hwnd, 0, 0, xsize, ysize, True)


def get_img(sct, x_min, x_size, y_min, y_size):
    img = np.array(sct.grab({"left": x_min, "width": x_size, "top": y_min, "height": y_size}))
    return img
