import pyttsx3 as tts

def speak(text):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()