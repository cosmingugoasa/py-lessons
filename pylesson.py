import speech_recognition as sr 
import pyttsx3
import sys
import subprocess
import os
import datetime
import shutil

FFMPEG_FILE_PATH = os.path.abspath("ffmpeg.exe")
AUDIO_FILE_PATH = os.path.abspath(sys.argv[-1])

files_outputted = 1

#check if audio.wav already exists and delete it
if(os.path.isfile("audio.wav")):
    print("**'audio.wav' already exists. Deleting it.**")
    os.remove("audio.wav")

#check if chucks/ has file and clean it
if(os.path.isdir('chunks')):
    print("**'chunks/' already exists. Emptying it.**")
    shutil.rmtree("chunks")
    os.mkdir("chunks")
else:
    os.mkdir("chunks")

#extract wav audio file from mkv video file
extractionTask = subprocess.run(f"{FFMPEG_FILE_PATH} -i {AUDIO_FILE_PATH} -ab 160k -ac 2 -ar 44100 -vn audio.wav", shell=True)

if(extractionTask.returncode != 0):
    print("**Error extracting audio**")
    sys.exit()
else:
    print("** Audio file extracted succesfully **")
    print("** Splitting audio chunks **")

#splitting main audio file into chunks for faster processing    
splittingTask = subprocess.run(f"{FFMPEG_FILE_PATH} -i audio.wav -f segment -segment_time 60 -c copy chunks/%03d.wav", shell=True)

if(splittingTask.returncode != 0):
    print("** Error while splitting **")
    sys.exit()
else:
    print("** Split succesful **")
    
#order file for stt
audio_chunks = []
for audio_chunk_filename in os.listdir('chunks/'):
    if(audio_chunk_filename.endswith(".wav")):
        audio_chunks.append(audio_chunk_filename)
audio_chunks.sort()
print(f"**{len(audio_chunks)} audio chunks created**")

#perform stt on each file
instance = sr.Recognizer()
stt_chunks = [] #stt of each chunk
count = 1
for chunk in audio_chunks:
    audioFile = sr.AudioFile((f"chunks/{chunk}"))
    
    with audioFile as source:
        instance.pause_threshold = 30
        print(f"** In ascolto : {count}/{len(audio_chunks)}**")
        audio = instance.listen(source)
        print("** Elaborazione **")                    
        
        try:
            stt_chunk = instance.recognize_google(audio, language="it-IT")
            stt_chunk = stt_chunk.lower()
            stt_chunks.append(stt_chunk)
        except Exception as e:
            print(f"**Could not understand audio. {e}**")

    count += 1

#write chunks to file
print("** Writing to file **")
dateString = datetime.datetime.now()
dateString = str(dateString)[:10]
output = open(f"lezione-{dateString}-{files_outputted}.txt", "a")
for chunk in stt_chunks:
    output.write(chunk + '\n')

output.close()

print("** DONE **")
print(f"**{files_outputted} lezioni create**")