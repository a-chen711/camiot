
import pyttsx3
from threading import *
import time


class v2(Thread):
	engine=None
	def __init__(self):
		self.engine = pyttsx3.init()
		rate = self.engine.getProperty('rate')
		self.engine.setProperty('rate', rate+20)
	def start(self,text):
		#time.sleep(0.4)
		self.engine.say(text)
		self.engine.runAndWait()




'''
class _TTS:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()
'''



