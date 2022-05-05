import time
import tensorflow as tf
import numpy as np
import cv2
import mss
import screen
import keys

x_size, y_size = screen.move_window_0('art of rally')

model = tf.keras.models.load_model('model_alpha_best')

with mss.mss() as sct:
    i = 0
    while not keys.check_quit_key():
        # resolution 1280 x 720, x_size x y_size is 1296 x 759
        # 1296 / 2 = 648
        img = screen.get_img(sct, 392, 512, 127, 512)
        img = cv2.resize(img, (128, 128))
        img = np.array([img[:, :, [2, 1, 0]]])

        k = ((model.predict(img) > 0.5) * 1)[0]
        keys.set_keys(k)
        time.sleep(0.1)

exit(0)

