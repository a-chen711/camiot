# Project CamIoT
UCLA Human Computer Interaction Lab

Project CamIoT is a wrist-mounted device that interacts with appliances via camera-captured finger motions. The project utilizes a
Raspberry Pi Zero W and a Raspberry Pi IR Camera. The user activates the camera by performing an up swing motion from their side so that
their ending position is parallel to the ground. The IMU recognizes the motion and initiates the camera to take photos of the finger 
movement and also to recognize the appliance that the finger points at. The appliance is recognized by performing data augmentation on test
photos taken prior to the usage of Project CamIoT and running the photos through a VGG19 Neural Network and MLP Classifier to identify the
appliance. Once the camera is initialized, it uses IR lamps on the side of the camera to illuminate the finger and after applying an IR
filter, the finger direction can be discerned and uploaded to the server for communication to the appliance. 
