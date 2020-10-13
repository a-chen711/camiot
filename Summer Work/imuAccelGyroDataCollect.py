from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)


def writeData(dataFile, sensorData, curTime):
    dataFile.write(str(curTime))
    dataFile.write(", ")
    dataFile.write(str(sensorData['x']))
    dataFile.write(", ")
    dataFile.write(str(sensorData['y']))
    dataFile.write(", ")
    dataFile.write(str(sensorData['z']))
    dataFile.write(",")
    dataFile.write("\n")


def getDataLoop(imuAccelDataTxt, imuGyroDataTxt):
    recordTime = int(input("How long do you want to record data? "))
    print("Recording for", recordTime, " seconds")
    print("Time,", "x-axis", "y-axis", "z-axis")

    startTime = time.time()
    curTime = 0.0

    while curTime < recordTime:
        accelData = sensor.get_all_data()[0]
        gyroData = sensor.get_all_data()[1]
        print(curTime, accelData, gyroData)
        writeData(imuAccelDataTxt, accelData, curTime)
        writeData(imuGyroDataTxt, gyroData, curTime)

        curTime = time.time() - startTime
        time.sleep(0.1)


def main():
    try:
        imuAccelDataTxt = open("imuAccelData.txt", "a")
        imuGyroDataTxt = open("imuGyroData.txt", "a")
    except IOError:
        print("ERROR: File not open!")

    getDataLoop(imuAccelDataTxt, imuGyroDataTxt)

    imuAccelDataTxt.close()
    imuGyroDataTxt.close()


if __name__ == "__main__":
    main()




