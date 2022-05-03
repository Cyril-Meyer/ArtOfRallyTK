import numpy as np
import matplotlib.pyplot as plt
import cv2

codename = 'test'

data_images = np.load(f'./self-driving/data/{codename}_images.npy')
data_keys = np.load(f'./self-driving/data/{codename}_keys.npy')

print(data_images.shape)
plt.imshow(cv2.cvtColor(data_images[0, :, :, 0:3], cv2.COLOR_BGR2RGB))
plt.show()