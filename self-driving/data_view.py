import time
import numpy as np
import cv2

codename = 'FIN_LAS_R_MOR_01'

data_images = np.load(f'./self-driving/data/{codename}_images.npy')
data_keys = np.load(f'./self-driving/data/{codename}_keys.npy')
data_memory = np.load(f'./self-driving/data/{codename}_memory.npy')

print(data_images.shape)
print(data_keys.shape)
print(data_memory.shape)

for i in range(len(data_images)):
    img = data_images[i, :, :]
    keys = data_keys[i]
    memory = data_memory[i]
    cv2.putText(img, f'Z', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, 2)
    cv2.putText(img, f'Q', (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, 2)
    cv2.putText(img, f'S', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, 2)
    cv2.putText(img, f'D', (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, 2)
    if keys[0] == 1:
        cv2.putText(img, f'Z', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    if keys[1] == 1:
        cv2.putText(img, f'Q', (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    if keys[2] == 1:
        cv2.putText(img, f'S', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    if keys[3] == 1:
        cv2.putText(img, f'D', (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    cv2.putText(img, f'{str(round(memory[0], 2)).rjust(6)}', (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    if memory[1] >= 0:
        cv2.putText(img, f'+{str(round(memory[1], 2))}', (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    else:
        cv2.putText(img, f'-{str(round(memory[1], 2))[1:]}', (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)
    cv2.imshow("data_view", img)

    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

    time.sleep(0.01)
cv2.destroyAllWindows()
