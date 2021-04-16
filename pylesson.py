import speech_recognition as sr 
import pyttsx3

instance = sr.Recognizer()

with sr.Microphone() as mic:
    instance.adjust_for_ambient_noise(mic, duration=.4)
    print("** In ascolto ... **")
    audio = instance.listen(mic)
    print("** Elaborazione ... **")

    text = instance.recognize_google(audio, language="it-IT")
    text = text.lower()

    print(f"Result : \n {text}")