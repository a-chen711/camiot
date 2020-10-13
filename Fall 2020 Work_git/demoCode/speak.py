import sys
import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+50)
    return engine

def say(s):
    engine.say(s)
    engine.runAndWait() #blocks

engine = init_engine()
say(str(sys.argv[1]))

 

