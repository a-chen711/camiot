from tts_watson.TtsWatson import TtsWatson

ttsWatson = TtsWatson('watson_user', 'watson_password', 'en-US_AllisonVoice') 
ttsWatson.play("Hello World")
