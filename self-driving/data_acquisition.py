import time
import numpy as np
import mss
import screen
import keys


# move window for acquisition
screen.move_window_0('art of rally')

print('prepare for data acquisition')

# data acquired
data_images = []
data_keys = []

# time before acquisition
time.sleep(5)

print('data acquisition begin')

with mss.mss() as sct:
    i = 0
    while i < 30:
        data_images.append(screen.get_img(sct, 112, 512, 50, 384))
        data_keys.append(keys.get_keys())
        time.sleep(0.5)
        i += 1

print('data acquisition ended')

codename = str(int(time.time()))
codename = 'test'
data_images = np.array(data_images)
data_keys = np.array(data_keys)


np.save(f'./self-driving/data/{codename}_images', data_images)
np.save(f'./self-driving/data/{codename}_keys', data_keys)

print('data saved')
