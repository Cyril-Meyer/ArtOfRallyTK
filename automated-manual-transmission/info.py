import numpy as np
import mss
from utils import videocapture


def set_window_position():
    x_size, y_size = videocapture.move_window_0('art of rally')
    # resolution 1280 x 720, x_size x y_size is 1296 x 759
    assert (x_size == 1296) and (y_size == 759)


def get_screen():
    with mss.mss() as sct:
        img = videocapture.get_img(sct, 490, 288, 710, 32)
        return img
    return None


def get_speed_img(img):
    return (np.average(img[:, 0:42], axis=-1) > 200)*1.0


def get_speed_digits(img):
    return np.stack([img[:, 0:12],
                     img[:, 14:14 + 12],
                     img[:, 28:28 + 12]])


def get_speed_digit(img, n):
    if n == 2:
        return img[:, 0:12]
    elif n == 1:
        return img[:, 14:14 + 12]
    elif n == 0:
        return img[:, 28:28+12]
    else:
        raise NotImplementedError


def get_gear_img(img):
    return (img[:, 100:100+20, 2] > 200)*1.0


def get_gear_digit(img):
    return img[:, 2:14]
