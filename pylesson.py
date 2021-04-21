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
import utility.file_renamer as util
import utility.gui as gui
from colorama import Fore 

FFMPEG_FILE_PATH = "ffmpeg.exe"
VIDEO_FOLDER_PATH = "D:/Documents/Destream/destreamer/videos"
DESTREAM_PATH = "D:/Documents/Destream/destreamer"
STUDENT_MAIL = "cosmin.gugoasa@studenti.unipr.it"

files_outputted = 0
max_threads_count = 4
main_working_dir = os.getcwd()


gui.printMenu()

############ DESTREAMER INTEGRATION #############
menuChoice = input()

os.chdir(DESTREAM_PATH)
if(menuChoice == "1"):
    print("Inserisci il link alla lezione: ")
    link = input()
    mkvExtractionTask = subprocess.run(f"destreamer.cmd -u {STUDENT_MAIL} -i {link}", shell=True)
elif(menuChoice == "2"):
    print("Inserisci il nome/percorso del file txt: ")
    txtFile = input()
    mkvExtractionTask = subprocess.run(f"destreamer.cmd -u {STUDENT_MAIL} -f {txtFile}", shell=True)
else:
    print(Fore.RED + "- Opzione non valida" + Fore.RESET)
    sys.exit()   

if(mkvExtractionTask.returncode != 0):
    print(Fore.RED + "- Failed to download mkv file" + Fore.RESET)
    sys.exit()
else:
    print(Fore.GREEN + "- Videos downloaded" + Fore.RESET)

os.chdir(main_working_dir)
#################################################

#file name normalization (basically replaces spaces in the name with _)
util.normalize_files_name(VIDEO_FOLDER_PATH)

#get ordered list of video files
raw_video_filename = []
for raw_video in os.listdir(f"{VIDEO_FOLDER_PATH}"):
    if(raw_video.endswith(".mkv")):
        raw_video_filename.append(raw_video)
raw_video_filename.sort()

#check if chunks/ has files and clean it
if(os.path.isdir(f"chunks/{files_outputted}")):
    print(Fore.CYAN + "- 'chunks/' already exists. Emptying it." + Fore.RESET)
    shutil.rmtree("chunks")
    os.mkdir("chunks")
    
for file in raw_video_filename :
    print(file)
    #check if audio.wav already exists and delete it
    if(os.path.isfile("audio.wav")):
        print(Fore.CYAN + "- updating audio file for stt splitting&extraction" + Fore.RESET)
        os.remove("audio.wav")

    #make folder for each lesson's chunks
    if not (os.path.exists(f"chunks/{files_outputted}")):
        os.mkdir(f"chunks/{files_outputted}")

    #extract wav audio file from mkv video file
    extractionTask = subprocess.run(f"{FFMPEG_FILE_PATH} -i {VIDEO_FOLDER_PATH}\{file} -ab 160k -ac 2 -ar 44100 -vn audio.wav", shell=True)

    if(extractionTask.returncode != 0):
        print(Fore.RED + "- Error extracting audio" + Fore.RESET)
        sys.exit()
    else:
        print(Fore.GREEN + "- audio file extracted succesfully. splitting audio chunks" + Fore.RESET)

    #splitting main audio file into chunks for faster processing    
    splittingTask = subprocess.run(f"{FFMPEG_FILE_PATH} -loglevel quiet -nostats -i audio.wav -f segment -segment_time 90 -c copy chunks/{files_outputted}/%03d.wav", shell=True)

    if(splittingTask.returncode != 0):
        print(Fore.RED + "- Error while splitting" + Fore.RESET)
        sys.exit()
    else:
        print(Fore.GREEN + "- split succesful" + Fore.RESET)
        
    #order file for stt
    audio_chunks = []
    for audio_chunk_filename in os.listdir(f"chunks/{files_outputted}"):
        if(audio_chunk_filename.endswith(".wav")):
            audio_chunks.append(audio_chunk_filename)
    audio_chunks.sort()
    print(Fore.CYAN + f"- {len(audio_chunks)} audio chunks created" + Fore.RESET)

    #perform stt on each file
    instance = sr.Recognizer()
    stt_chunks = [None] * (len(audio_chunks)-1) #stt of each chunk
    count = 0
    #pbar = tqdm(total=10 +1)
    pbar = tqdm(total=len(audio_chunks))

    for chunk in audio_chunks:
        while(threading.active_count() > max_threads_count + 1):
            time.sleep(0.1)
        
        audioFile = sr.AudioFile((f"chunks/{files_outputted}/{chunk}"))

        t = threading.Thread(target=stt.recog, args=(audioFile, instance, count, audio_chunks, stt_chunks,))
        t.start()

        pbar.update(1)
        count += 1
        
        #if(count == 10):
        #    break

    while(threading.active_count() > 2):
        time.sleep(0.1)

    pbar.update(1)
    pbar.close()

    #write chunks to file
    print("- writing to file")
    dateString = datetime.datetime.now()
    dateString = str(dateString)[:10]
    output = open(f"lezione-{dateString}-{files_outputted}.txt", "a")
    for chunk in stt_chunks:
        if(chunk != None):
            output.write(chunk + '\n')

    output.close()
    files_outputted += 1

print(Fore.GREEN + f"- Done " + Fore.RESET)

################# CLEAN UP #####################
print(Fore.GREEN + f"- Clean up started" + Fore.RESET)
shutil.rmtree(VIDEO_FOLDER_PATH)

print(Fore.MAGENTA + f"Close window, and go study" + Fore.RESET)