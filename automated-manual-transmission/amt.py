import argparse
import json
import time
import tensorflow as tf
import numpy as np
import cv2
import info


parser = argparse.ArgumentParser()
parser.add_argument('settings', help='json file containing gearbox settings',
                    type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()
gearbox = json.load(args.settings)
print(gearbox, type(gearbox))

info.set_window_position()

model = tf.keras.models.load_model('automated-manual-transmission/model_ocr_speed')

cv2.namedWindow('capture')
cv2.moveWindow('capture', 1400, 0)
fps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
speed = 0
gear = 0
rpm = 0

while True:
    t0 = time.time()
    flag_no_error = True

    if cv2.waitKey(1) & 0Xff == 27:
        break

    # read screen
    img = info.get_screen()
    # select speed and gear area
    speed_img = info.get_speed_img(img)
    gear_img = info.get_gear_img(img)
    # OCR speed and gear
    speed_digits = info.get_speed_digits(speed_img)
    gear_digit = info.get_gear_digit(gear_img)
    X = np.concatenate([speed_digits, [gear_digit]], axis=0)
    Y = np.argmax(model(X), axis=-1)
    Y_speed = Y[0:3]
    Y_gear = Y[3]
    # check for error in values
    if (Y_gear < 1) or (5 < Y_gear < 11) or np.any(Y_speed > 10):
        flag_no_error = False

    # select rpm area
    rpm_img = info.get_rpm_img(img)
    # recognize
    Y_rpm = info.get_rpm_digits(rpm_img)
    if np.any(np.diff(Y_rpm) > 0):
        flag_no_error = False

    if not flag_no_error:
        print("ERROR :", Y, Y_rpm)
    else:
        gear = Y_gear
        speed = (Y_speed[0] % 10) * 100 +\
                (Y_speed[1] % 10) * 10 +\
                (Y_speed[2] % 10)
        rpm = max(1000, (np.max(np.argwhere(Y_rpm[0:-1])))*1000)

    # print info
    capture = np.zeros((img.shape[0]+64, img.shape[1], 3), dtype=img.dtype)
    capture[0:img.shape[0], 0:img.shape[1], :] = img
    cv2.putText(capture, f'{speed:03}', (10, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
    cv2.putText(capture, f'{gear}', (100, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
    cv2.putText(capture, f'{rpm:04}', (150, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
    cv2.putText(capture, f'FPS : {round(np.average(fps))}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, 2)
    cv2.imshow('capture', capture)

    t1 = time.time()
    fps = fps[1:]
    fps.append(round(1 / (t1 - t0)))

cv2.destroyAllWindows()
