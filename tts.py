import pyttsx3 as tts
import threading

def speak(text):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()