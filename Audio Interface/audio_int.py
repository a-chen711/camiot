import pyttsx3

def ask(obj, qnum): #ask for input from user using text input for now but can replace with the input from the camiot later
	print('qnum = ' + str(qnum))
	while True:
		if qnum == 1:
			choice = input("on, off, or repeat: ")
			break
		if obj == 'TV':
			if (qnum == 2): #volume or channel?
				choice = input("volume, channel, rechoose, repeat: ")
				break
			elif (qnum == 3):
				choice = input("up, down, rechoose, repeat: ")
				break
		elif obj == 'Printer':
			if qnum == 2:
				choice = input("print or rechoose for (on/off): ")
				break
		elif obj == 'Lamp':
			if qnum == 2:
				choice = input('bright, dark, or rechoose for (on/off): ')
				break
		elif obj == 'CoffeeMaker':
			if qnum == 2:
				choice = input('brew or rechoose for (on/off): ')
				break
		elif obj == 'Toaster':
			if qnum == 2:
				choice = input('toast or rechoose for (on/off): ')
				break
	return choice


def audio_interface(obj):
#pass in a string that defines the object
	engine = pyttsx3.init()
	engine.say('You have chosen the '+obj)
	engine.runAndWait()
	while (True):
		qnum = 1
		engine.say('Please Point left for On and right for Off')
		engine.runAndWait()
		choice = ask(obj, qnum) #input answer
		#execute this command
		qnum +=1

		if choice == "on":
			engine.say("Turning the " + obj + " on")
			engine.runAndWait()
			#execute this command
		elif choice == 'repeat':
			qnum -=1
			continue
		else:
			engine.say('Shutting Down the ' + obj)
			engine.runAndWait()
			exit()
		if obj == 'TV':
				while(True):
					engine.say('Point left for Volume, right for Channel, up to choose on or off, or down to repeat the question')
					engine.runAndWait()
					choice = ask(obj, qnum) 
					#execute answer
					if choice == 'rechoose':
						qnum -=1
						break 
					qnum += 1
					if choice == "volume":
						engine.say('You have chosen ' + choice)
						engine.runAndWait()
						while(True):
							engine.say('Point left for Volume Up, right for Volume Down, up to choose volume or channel, or down to repeat the question')
							engine.runAndWait()
							choice= ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum -=1
								break
					elif choice == "channel":
						engine.say('You have chosen ' + choice)
						engine.runAndWait()
						while(True):
							engine.say('Point left for Channel Up, right for channel down, up to choose volume or channel, or down to repeat the question')
							engine.runAndWait()
							choice = ask(obj, qnum) 
							#execute answer
							if choice == 'rechoose':
								qnum-=1
								break
					elif choice == 'repeat':
						qnum -=1
						continue
					continue
				continue
		elif obj == 'Printer':
			while(True):
					engine.say('Point left to Print, right to choose on or off, or down to repeat the question')
					engine.runAndWait()
					choice = ask(obj, qnum) 
					#execute answer
					if choice == 'rechoose':
						qnum -=1
						break 
					elif choice == 'print':
						engine.say('printing now')
						engine.runAndWait()
						#execute print job 
					elif choice == 'repeat':
						qnum -=1
						continue
			continue
		elif obj == 'Lamp':
			while(True):
					engine.say('Point left for brighter, right for darker, up to choose on or off, or down to repeat the question')
					engine.runAndWait()
					choice = ask(obj, qnum) 
					#execute answer
					if choice == 'rechoose':
						qnum -=1
						break 
					elif choice == 'bright' or choice == 'dark':
						engine.say('Making the light ' + choice + 'er')
						engine.runAndWait()
						#execute command 
					elif choice == 'repeat':
						qnum -=1
						continue
			continue
		elif obj == 'CoffeeMaker':
			while(True):
					engine.say('Point left to brew coffee, right to choose on or off, or down to repeat the question')
					engine.runAndWait()
					choice = ask(obj, qnum) 
					#execute answer
					if choice == 'rechoose':
						qnum -=1
						break 
					elif choice == 'brew':
						engine.say('Brewing coffee now')
						engine.runAndWait()
						#execute command 
					elif choice == 'repeat':
						qnum -=1
						continue
			continue
		elif obj == 'Toaster':
			while(True):
					engine.say('Point left to start toasting, right to choose on or off, or down to repeat the question')
					engine.runAndWait()
					choice = ask(obj, qnum) 
					#execute answer
					if choice == 'rechoose':
						qnum -=1
						break 
					elif choice == 'toast':
						engine.say('Toasting now')
						engine.runAndWait()
						#execute command 
					elif choice == 'repeat':
						qnum -=1
						continue
			continue
		
audio_interface(input("What appliance? TV, Printer, Lamp, CoffeeMaker, or Toaster "))
