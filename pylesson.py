import speech_recognition as sr 
import pyttsx3
import sys
import subprocess
import os
import datetime

FFMPEG_FILE_PATH = os.path.abspath("ffmpeg.exe")
AUDIO_FILE_PATH = os.path.abspath(sys.argv[-1])

#print(os.path.abspath(AUDIO_FILE_PATH))
#os.system(f"{FFMPEG_FILE_PATH} -i {AUDIO_FILE_PATH} -ab 160k -ac 2 -ar 44100 -vn audio.wav")
task = subprocess.run(f"{FFMPEG_FILE_PATH} -i {AUDIO_FILE_PATH} -ab 160k -ac 2 -ar 44100 -vn audio.wav", shell=True)

if(task.returncode == 0):
    print("** Audio file extracted succesfully **")
    #print(os.path.abspath("audio.wav"))

    instance = sr.Recognizer()
    audioFile = sr.AudioFile("test_audio.wav")

    try:
        with audioFile as source:
            instance.pause_threshold = 5.0
            print("** In ascolto ... **")
            audio = instance.listen(source)
            print("** Elaborazione ... **")

            text = instance.recognize_google(audio, language="it-IT")
            text = text.lower()

            print(f"Result : \n {text}")

            #get date string to add in output file name
            dateString = datetime.datetime.now()
            dateString = str(dateString)[:10]
            
            #creating output file
            output = open(f"lezione-{dateString.split(' ')[0]}.txt", "a")
            output.write(text)
            output.close()

    except Exception as e:
        print(e)

else:
    print("** Couldn't extract audio file **")



