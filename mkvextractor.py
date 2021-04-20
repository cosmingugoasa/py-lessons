import os
import subprocess
import sys
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link", type=str, metavar=" ", help="link to the lesson")
parser.add_argument("-f", "--file", type=str, metavar=" ", help="txt file with the links")

args = parser.parse_args()

link = args.link
txtFile = args.file

DESTREAM_PATH = "D:\Documents\Destream\destreamer"
STUDENT_MAIL = "cosmin.gugoasa@studenti.unipr.it"
#link = "https://web.microsoftstream.com/video/ddcdf8ed-8046-4047-aeff-d93ca0a6da64?referrer=https:%2F%2Felly2020.dia.unipr.it%2F"

os.chdir(DESTREAM_PATH)

if(link != None):
    mkvExtractionTask = subprocess.run(f"destreamer.cmd -u {STUDENT_MAIL} -i {link}", shell=True)
elif(txtFile != None):
        mkvExtractionTask = subprocess.run(f"destreamer.cmd -u {STUDENT_MAIL} -f {txtFile}", shell=True)
else:
    print("**No valid input. Run mkvextractor.py -h for help**")
    sys.exit()

if(mkvExtractionTask.returncode != 0):
    print("**Failed to download mkv file**")

else:
    print("**Videos downloaded**")
