import random
import time
from imuTrigArr6 import trigger 

def get_flag(flag_list):
    return random.choice(flag_list)


def countdown(current_flag):
    print('\n')

    print(f'Start ** {current_flag} ** gesture in...')

    for i in range(0,3):
        print(i)
        time.sleep(0.8)
    print('\n')
    print('recording data...')


imuData = open("imuData-7-24-20.txt", "a")

active = True
counter = 0
label = ""
tCount = 0
fCount = 0

num_data_points = 0
num_true_input = 0

num_data_points = int(input('Tell us the number of data points to record:'))
num_true_input = int(input('Tell us how many true gestures you want to record:'))

# create a list of flags that represent how many true's and false you want to record
# in a flag or a current gesure is randomly selected and returned then the user is
# told to preform that gesture and then is given a count down in theory this should
# result in the correct amount of trues and falses I did this because I'm lazy

flag_list = [True] * num_true_input + [False] * (num_data_points - num_true_input)
delay = 0.1
sps = int(1/delay) #samples per second


for i in range(0, num_data_points):
    print('\n')
    print("Number of True's: ", tCount, " Number of False's: ", fCount)
    flags = []

    current_flag = get_flag(flag_list)

    if current_flag:
        label = "RAISED"
        tCount += 1
    else:
        label = "NOT_RAISED"
        fCount += 1

    countdown(current_flag)

    imuData.write("\n")
    imuData.write(label)
    imuData.write(", ")
    # imuData.write(str(counter))
    # imuData.write(", ")
    startTime = time.time()

    while (time.time() - startTime) < 3.0:
        arm_raised = trigger(flags, delay, sps)
        print(arm_raised)
        imuData.write(str(arm_raised))
        imuData.write(", ")
        time.sleep(delay)

