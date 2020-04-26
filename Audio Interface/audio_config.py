import json 
import pyttsx3
path = 'config.json' #adjust as needed
#Globally used Appliance list
######################
with open(path, "r") as infile: 
    data = json.load(infile)
num_appliances = len(data["appliance"])
appliance_list = []
for i in range(num_appliances):
	appliance_list.append(data["appliance"][i]["appliance_name"])
######################

#returns the functions of the given appliance
def get_functions(appliance):
	appliance_ind = appliance_list.index(appliance)
	num_functions = len(data["appliance"][appliance_ind]["functions"])
	function_list = []
	for i in range(num_functions):
		function_list.append(data["appliance"][appliance_ind]["functions"][i])
	return function_list, num_functions
######################

def get_operations(appliance, function):
	function_list, num_functions = get_functions(appliance)
	appliance_ind = appliance_list.index(appliance)
	function_ind = function_list.index(function)
	num_operations = len(data["appliance"][appliance_ind]["operations_" + str(function_ind+1)]) #get the length of operation list
	operation_list = []
	for i in range(num_operations):
		operation_list.append(data["appliance"][appliance_ind]["operations_" + str(function_ind+1)][i])
	return operation_list, num_operations
######################

def ask(obj, function, qnum):
	print('qnum = ' + str(qnum))
	while True:
		if qnum == 1:
			print("Type one of the following: ")
			for i in range(num_appliances):
				print(appliance_list[i])
			choice = input()
			break
		elif qnum == 2:
			choice = input("on, off, return, repeat: ")
			break
		elif qnum == 3:
			functions, num_functions = get_functions(obj)
			print("Type one of the following: ")
			for i in range(num_functions):
				print(functions[i])
			print('return\nrepeat')
			choice = input()
			break
		elif qnum == 4:
			operations, num_operations = get_operations(obj, function)
			print("Type one of the following: ")
			for i in range(num_operations):
				print(operations[i])
			print('return\nrepeat')
			choice = input()
			break
	return choice
  


#May need to adjust dialogue of functions based on the function you use. 
def audio_int():
	engine = pyttsx3.init()
	while True:
		engine.say('Choose an appliance to interact with')
		engine.runAndWait()
		obj = ask(None, None, 1)
		#input answer
		if obj in appliance_list:
			engine.say('You have chosen the '+obj)
			engine.runAndWait()
			while True:
				qnum = 2
				engine.say('Please Point left for On, right for Off, up to choose the appliance again, or down to repeat the question')
				engine.runAndWait()
				choice = ask(obj, None, qnum)
				if choice == "on":
					engine.say("Turning the " + obj + " on")
					engine.runAndWait()
					#TURNING THE APPLIANCE ON
				elif choice == 'repeat':
					continue
				elif choice == 'return': #going up to the previous question
					break
				else:
					engine.say('Shutting Down the ' + obj)
					engine.runAndWait()
					exit()
					#TURNING THE APPPLIANCE OFF
				functions, num_functions = get_functions(obj)
				#Acquire all the functions of the appliance chosen
				while True:
					qnum = 3
					if num_functions == 1: 
						engine.say('Point left to choose ' + functions[0] + ', up to choose on or off, or down to repeat the question')
						engine.runAndWait()
						choice = ask(obj, None, qnum)
						if choice == 'return':
							break 
						elif choice == functions[0]: #if there is only one function, can split into two branches for operations or just one for one operation
							operations, num_operations = get_operations(obj, choice)
							while True:
								qnum = 4
								if num_operations == 1: #if there is only one operation and one function(ie brew, print, toast)
									engine.say(operations[0] + 'ing now') 
									engine.runAndWait()
									#execute answer
									break
								elif num_operations == 2: #if there is only one function but two functions (ie adjust brightness, brighter or darker)
									engine.say('Point left to choose ' + operations[0] + ', right to choose ' + operations[1] + ', up to return, and down to repeat the question')
									engine.runAndWait()
									choice = ask(obj, functions[0], qnum) #qnum is 4 at this point
									#execute answer
									if choice == 'return':
										break 
									elif choice == operations[0] or choice == operations[1]:
										engine.say(choice + 'ing now')
										engine.runAndWait()
										#execute answer
									elif choice == 'repeat':
										continue
						elif choice == 'repeat':
							continue
					elif num_functions == 2: #if the number of functions for that appliance is 2 
						engine.say('Point left to choose ' + functions[0] + ', right to choose ' + functions[1] + ', up to choose on or off, or down to repeat the question')
						engine.runAndWait()
						choice = ask(obj, None, qnum)
						if choice == 'return':
							break
						elif choice == functions[0] or choice == functions[1]:
							operations, num_operations = get_operations(obj, choice)
							curr_function = choice  # have to store the curr_function we're using in the event of returning after choosing another function(ie 1st choose volume, return and choose channel)
							while True:
								qnum = 4
								if num_operations == 1: #if there is only one operation and but 2 functions(No example yet but could be used)
									engine.say(operations[0] + 'ing now')     ##### may need to adjust dialogue based on the operations you add
									engine.runAndWait()
									#execute answer
									break
								elif num_operations == 2: #if there is only one function but two functions (ie adjust brightness, brighter or darker)
									engine.say('Point left to choose ' + operations[0] + ', right to choose ' + operations[1] + ', up to return, and down to repeat the question')
									engine.runAndWait()
									choice = ask(obj, curr_function, qnum)
									#execute answer
									if choice == 'return':
										break 
									elif choice == operations[0] or choice == operations[1]:
										engine.say('You have chosen ' + choice)
										engine.runAndWait()
										#execute answer
									elif choice == 'repeat':
										continue
						elif choice == 'repeat':
							continue
		elif obj == 'q':
			exit()
		else:
			engine.say('Please choose a valid appliance')
			engine.runAndWait()

#audio_int()
