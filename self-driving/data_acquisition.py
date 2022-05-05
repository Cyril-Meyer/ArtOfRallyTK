import time
import numpy as np
import cv2
import mss

import screen
import keys
import dashboard.dashboard as dashboard


# user choice
CODENAME = str(int(time.time()))
CODENAME = 'FIN_LAS_R_MOR_01'

# memory data
pm = dashboard.open_aor_process()
addresses = dashboard.get_addresses_selection('cheat-table/artofrally.CT', pm, ['Speed pointer 1', 'Steering pointer 1'])
print(addresses)
addresses_pointer = []
addresses_type = []

for k in addresses.keys():
    addresses_pointer.append(addresses[k][0])
    addresses_type.append(addresses[k][1])

# move window for acquisition
x_size, y_size = screen.move_window_0('art of rally')
print(x_size, y_size)

print('prepare for data acquisition')

# data acquired
data_images = []
data_keys = []
data_memory = []

# time before acquisition
time.sleep(5)

print('data acquisition begin')

with mss.mss() as sct:
    i = 0
    while not keys.check_quit_key():
        # resolution 1280 x 720, x_size x y_size is 1296 x 759
        # 1296 / 2 = 648
        img = screen.get_img(sct, 392, 512, 127, 512)
        img = cv2.resize(img, (256, 256))
        data_images.append(img)
        data_keys.append(keys.get_keys())
        mem = []
        for j in range(len(addresses_pointer)):
            mem.append(dashboard.get_value(addresses_pointer[j], addresses_type[j], pm))
        data_memory.append(mem)
        time.sleep(0.1)
        i += 1

print('data acquisition ended')

data_images = np.array(data_images)
data_keys = np.array(data_keys)
data_memory = np.array(data_memory)

np.save(f'./self-driving/data/{CODENAME}_images', data_images)
np.save(f'./self-driving/data/{CODENAME}_keys', data_keys)
np.save(f'./self-driving/data/{CODENAME}_memory', data_memory)

print('data saved')
