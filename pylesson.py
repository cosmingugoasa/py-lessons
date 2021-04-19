import speech_recognition as sr 
import pyttsx3
import sys
import subprocess
import os
import datetime
import shutil
import stt
import threading
import time
from tqdm import tqdm

FFMPEG_FILE_PATH = os.path.abspath("ffmpeg.exe")
AUDIO_FILE_PATH = os.path.abspath(sys.argv[-1])

files_outputted = 1
max_threads_count = 4

#################################################
#   MAIN
#################################################

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

#make folder for each lesson's chunks
if not (os.path.exists(f"chunks/{files_outputted}")):
    os.mkdir(f"chunks/{files_outputted}")

#extract wav audio file from mkv video file
extractionTask = subprocess.run(f"{FFMPEG_FILE_PATH} -i {AUDIO_FILE_PATH} -ab 160k -ac 2 -ar 44100 -vn audio.wav", shell=True)

if(extractionTask.returncode != 0):
    print("**Error extracting audio**")
    sys.exit()
else:
    print("** Audio file extracted succesfully **")
    print("** Splitting audio chunks **")

#splitting main audio file into chunks for faster processing    
splittingTask = subprocess.run(f"{FFMPEG_FILE_PATH} -i audio.wav -f segment -segment_time 90 -c copy chunks/{files_outputted}/%03d.wav", shell=True)

if(splittingTask.returncode != 0):
    print("** Error while splitting **")
    sys.exit()
else:
    print("** Split succesful **")
    
#order file for stt
audio_chunks = []
for audio_chunk_filename in os.listdir(f"chunks/{files_outputted}"):
    if(audio_chunk_filename.endswith(".wav")):
        audio_chunks.append(audio_chunk_filename)
audio_chunks.sort()
print(f"**{len(audio_chunks)} audio chunks created**")

#perform stt on each file
instance = sr.Recognizer()
stt_chunks = [None] * (len(audio_chunks)-1) #stt of each chunk
count = 0
#pbar = tqdm(total=10 +1)
pbar = tqdm(total=len(audio_chunks))

for chunk in audio_chunks:
    while(threading.active_count() > max_threads_count + 1):
        #print(f"**Waiting for a free thread**")
        time.sleep(0.1)
    
    audioFile = sr.AudioFile((f"chunks/{files_outputted}/{chunk}"))

    #stt.recog(audioFile, instance, count, audio_chunks, stt_chunks)
    t = threading.Thread(target=stt.recog, args=(audioFile, instance, count, audio_chunks, stt_chunks,))
    t.start()

    pbar.update(1)
    count += 1
    
    #if(count == 10):
    #    break

while(threading.active_count() > 2):
    #print(f"Active threads : {threading.active_count()}")
    time.sleep(0.1)

pbar.update(1)
pbar.close()

#write chunks to file
print("** Writing to file **")
dateString = datetime.datetime.now()
dateString = str(dateString)[:10]
output = open(f"lezione-{dateString}-{files_outputted}.txt", "a")
for chunk in stt_chunks:
    if(chunk != None):
        output.write(chunk + '\n')

output.close()

print("** DONE **")
print(f"**{files_outputted} lezioni create**")
