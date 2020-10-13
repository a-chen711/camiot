from mpu6050 import mpu6050
import time
import numpy as np
import tensorflow as tf

sensor = mpu6050(0x68)

def trigger():
    interpreter = tf.lite.Interpreter(model_path="gesture_model_v2.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    GESTURES = [
        "True",
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
                (accel_data['x'] + 14.2) / (14.2 * 2),
                (accel_data['y'] + 14.2) / (14.2 * 2),
                (accel_data['z'] + 14.2) / (14.2 * 2),
                (gyro_data['x'] + 250.2) / (250.2 * 2),
                (gyro_data['y'] + 250.2) / (250.2 * 2),
                (gyro_data['z'] + 250.2) / (250.2 * 2),
            ]

            gyro_data.clear()
            accel_data.clear()
            num_datapoints += 1
            time.sleep(0.05)

        inputs.append(tensor)
        inputsArr = np.array(inputs, dtype=np.float32)
        input_shape = input_details[0]['shape']
        interpreter.set_tensor(input_details[0]['index'], inputsArr)

        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        if output_data[0][0] > 0.8: #if true is 80% match, return true
            return True
        inputs.clear()
        return False




