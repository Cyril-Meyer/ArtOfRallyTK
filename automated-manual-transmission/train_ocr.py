import numpy as np
import tensorflow as tf

# Load OCR dataset
X_speed = np.load('automated-manual-transmission/dataset_ocr/speed_X.npy')
Y_speed = np.load('automated-manual-transmission/dataset_ocr/speed_Y.npy')
X_gear = np.load('automated-manual-transmission/dataset_ocr/gear_X.npy')
Y_gear = np.load('automated-manual-transmission/dataset_ocr/gear_Y.npy')

print(X_speed.shape, X_speed.dtype)
print(Y_speed.shape, Y_speed.dtype)
print(X_gear.shape, X_gear.dtype)
print(Y_gear.shape, Y_gear.dtype)


# Preprocess OCR dataset
def get_digit(number, n):
    return number // 10**n % 10


# Dataset storage
X = []
Y = []  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NULL, N, R
# Load speed (10 digits + NULL)
for i in range(len(X_speed)):
    x = X_speed[i]
    y = Y_speed[i]

    X.append(x[:, 0:12])
    if y >= 100:
        Y.append(get_digit(y, 2))
    else:
        Y.append(10)

    X.append(x[:, 14:14+12])
    if y >= 10:
        Y.append(get_digit(y, 1))
    else:
        Y.append(10)

    X.append(x[:, 28:28+12])
    Y.append(get_digit(y, 0))

# Load gear (5 digits + N + R)
X_gear = X_gear[:, :, 2:14]
Y_gear = np.where(Y_gear == 'N', 11, Y_gear)
Y_gear = np.where(Y_gear == 'R', 12, Y_gear)
Y_gear = Y_gear.astype(Y_speed.dtype)

for i in range(len(X_gear)):
    x = X_gear[i]
    y = Y_gear[i]
    X.append(x)
    Y.append(y)

# Transform input to numpy array
X = np.array(X).astype(np.float32)
Y = np.array(Y).astype(np.float32)
# Shuffle OCR dataset
p = np.random.permutation(len(X))
X = X[p]
Y = Y[p]
# Add channel (channel last)
X = np.expand_dims(X, -1)

# Dataset information
print(X.shape, X.dtype, X.min(), X.max())
print(Y.shape, Y.dtype, Y.min(), Y.max())
# Dataset split
X_train = X[0:8500]
Y_train = Y[0:8500]
X_test = X[8500:]
Y_test = Y[8500:]

# Classifier model
inputs = tf.keras.Input(shape=(32, 12, 1))
x = inputs
x = tf.keras.layers.Conv2D(16, 3, activation='relu')(inputs)
x = tf.keras.layers.Conv2D(16, 3, activation='relu')(x)
x = tf.keras.layers.Conv2D(16, 3, activation='relu')(x)
x = tf.keras.layers.Flatten()(x)
outputs = tf.keras.layers.Dense(13, activation='softmax')(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Compile and train
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

model.fit(X_train, Y_train, batch_size=16, epochs=100, validation_data=(X_test, Y_test))

model.save('automated-manual-transmission/model_ocr_speed')
