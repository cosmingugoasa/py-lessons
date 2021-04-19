import os
import subprocess
import sys
import shutil

DESTREAM_FOLDER_PATH = os.path.abspath("D:\Documents\Destream\destreamer")
DESTREAM_SH = "./destreamer.sh"
MKV_FILES_PATH = os.path.abspath("D:\Documents\Destream\destreamer\videos")
studentMail = "cosmindaxgugoasa@gmail.com"
TXT_LINKS_PATH = os.path.abspath("links.txt")

#./destreamer.sh -f D:\Documents\Dev\py-lessons\links.txt  -u cosmin.gugoasa@studenti.unipr.it
mkvExtractionTask = subprocess.run([f"cd {DESTREAM_FOLDER_PATH}", f"{DESTREAM_SH} -f {TXT_LINKS_PATH} -u {studentMail}"], shell=True)

if(mkvExtractionTask.returncode != 0):
    print("**Failed to download mkv file**")

else:
    print("**Videos downloaded**")
