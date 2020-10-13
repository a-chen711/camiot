from mpu6050 import mpu6050
import time
import numpy as np
import tensorflow as tf

sensor = mpu6050(0x68)

print("Starting...")

interpreter = tf.lite.Interpreter(model_path="gesture_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

GESTURES = [
    "Raise",
    "Roll",
    "False",
]

SAMPLES_PER_GESTURE = 16

inputs = []

gyro_data = []
accel_data = []


while True:

    num_datapoints = 0

    tensor = []

    while num_datapoints < 16:

        gyro_data = sensor.get_gyro_data()
        accel_data = sensor.get_accel_data()

        tensor += [
            (accel_data['x'] + 12.9) / (12.9 * 2),
            (accel_data['y'] + 12.9) / (12.9 * 2),
            (accel_data['z'] + 12.9) / (12.9 * 2),
            (gyro_data['x'] + 212.5) / (212.5 * 2),
            (gyro_data['y'] + 212.5) / (212.5 * 2),
            (gyro_data['z'] + 212.5) / (212.5 * 2),
        ]

        gyro_data.clear()
        accel_data.clear()
        num_datapoints += 1
        time.sleep(0.1)

    inputs.append(tensor)
    inputsArr = np.array(inputs, dtype=np.float32)
    input_shape = input_details[0]['shape']
    interpreter.set_tensor(input_details[0]['index'], inputsArr)

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    if output_data[0][0] > 0.8:
        print(GESTURES[0], ":", output_data[0][0])
        print(GESTURES[1], ":", output_data[0][1])

    inputs.clear()




