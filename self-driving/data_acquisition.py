import time
import numpy as np
import mss
import screen
import keys
import dashboard.dashboard as dashboard


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
screen.move_window_0('art of rally')

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
    while i < 300:
        data_images.append(screen.get_img(sct, 112, 512, 50, 384))
        data_keys.append(keys.get_keys())
        mem = []
        for j in range(len(addresses_pointer)):
            mem.append(dashboard.get_value(addresses_pointer[j], addresses_type[j], pm))
        data_memory.append(mem)
        time.sleep(0.1)
        i += 1

print('data acquisition ended')

codename = str(int(time.time()))
codename = 'test'
data_images = np.array(data_images)
data_keys = np.array(data_keys)
data_memory = np.array(data_memory)

np.save(f'./self-driving/data/{codename}_images', data_images)
np.save(f'./self-driving/data/{codename}_keys', data_keys)
np.save(f'./self-driving/data/{codename}_memory', data_memory)

print('data saved')
