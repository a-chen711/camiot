#Here goes the client code 

from newTriggerv2 import trigger

while True:
	print('Waiting...')
	if trigger():
		print('Triggered')