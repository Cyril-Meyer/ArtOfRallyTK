import time
import tensorflow as tf
import numpy as np
import cv2
import info

info.set_window_position()

model = tf.keras.models.load_model('automated-manual-transmission/model_ocr_speed')

cv2.namedWindow('capture')
cv2.moveWindow('capture', 1400, 0)

while True:
    t0 = time.time()
    flag_no_error = True

    if cv2.waitKey(1) & 0Xff == 27:
        break

    img = info.get_screen()
    speed_img = info.get_speed_img(img)
    gear_img = info.get_gear_img(img)

    speed_digits = info.get_speed_digits(speed_img)
    gear_digit = info.get_gear_digit(gear_img)
    X = np.concatenate([speed_digits, [gear_digit]], axis=0)
    Y = np.argmax(model(X), axis=-1)

    Y_speed = Y[0:3]
    Y_gear = Y[3]

    if (Y_gear < 1) or (5 < Y_gear < 11) or np.any(Y_speed > 10):
        flag_no_error = False

    if not flag_no_error:
        print("ERROR :", Y)
    else:
        gear = Y_gear
        speed = (Y_speed[0] % 10) * 100 +\
                (Y_speed[1] % 10) * 10 +\
                (Y_speed[2] % 10)
        print(gear, '-', speed)

    cv2.imshow('capture', img)

    t1 = time.time()
    print('FPS', round(1 / (t1 - t0)))

cv2.destroyAllWindows()
