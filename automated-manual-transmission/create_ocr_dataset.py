import time
import numpy as np
import cv2
import pytesseract
import info

time.sleep(2)

speed_X = []
speed_Y = []
gear_X = []
gear_Y = []

data = 0
data_required = 5000

while True:
    img = info.get_screen()
    speed_img = info.get_speed_img(img)
    gear_img = info.get_gear_img(img)

    speed = pytesseract.image_to_string((speed_img*255).astype(np.uint8), config='--psm 10')
    gear = pytesseract.image_to_string((gear_img*255).astype(np.uint8), config='--psm 10')

    speed = speed.replace(' ', '').replace('\n', '')
    gear = gear.replace(' ', '').replace('\n', '')

    if speed.isdigit():
        print(speed)
        speed = int(speed)
        speed_X.append(speed_img)
        speed_Y.append(speed)
        data += 1

    if (gear.isdigit() and 0 < int(gear) < 6) or gear in ['R', 'N']:
        print(gear)
        gear_X.append(gear_img)
        gear_Y.append(gear)
        data += 1

    if data >= data_required:
        break
    else:
        print((data / data_required)*100, '%')

np.save('automated-manual-transmission/dataset_ocr/speed_X.npy', np.array(speed_X))
np.save('automated-manual-transmission/dataset_ocr/speed_Y.npy', np.array(speed_Y))
np.save('automated-manual-transmission/dataset_ocr/gear_X.npy', np.array(gear_X))
np.save('automated-manual-transmission/dataset_ocr/gear_Y.npy', np.array(gear_Y))
