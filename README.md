# Project CamIoT
UCLA Human Computer Interaction Lab - Principal Investigator Xiang "Anthony" Chen.
In collaboration with Amirali Omidfar and Yuan Liang.

Project CamIoT is a wrist-mounted device that interacts with appliances via camera-captured finger motions. The project utilizes a
Raspberry Pi Zero W, a Raspberry Pi IR Camera, and a speaker. 
# Phase 1: Gesture Detection and Appliance Recognition
The user activates the camera by raising their arm from their side so as to point at an appliance. I trained the device with TensorFlow
Lite to recognize this motion over a few hundred trials. After detecting the user raising their arm, the device begins taking photos of the user's
extended index finger and the appliance the user is pointing at. The photo is sent via Socket to a server where the appliance is recognized
through a VGG-16 ConvNet that was pretrained with photos of the appliances. The appliance with highest probability of being correct is then 
sent back to the device. The recognized appliance is then spoken through the device's speaker and it enters phase 2. 
# Phase 2: Finger Detection
A continuous video capture is initiated once the appliance is recognized. Certain frames will be fetched from the video capture which will be used 
to recognize the finger and the direction it is pointing in. The frames will be analyzed using edge detection and a skin color filter to create 
isolated regions, in which the chosen largest region will be the user's finger. A base of the finger is established and then its angle is determined
by combing up the isolated region to find the midpoint of the finger tip and calculating gradient from the base midpoint. Once the angle is determined, 
the speaker will announce the function of that direction respective of the appliance chosen. To preserve accuracy, only 3 directions, Left, Middle, and Right
were used in this version. 
