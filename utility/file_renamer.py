import os
import sys

def normalize_files_name(video_folder_path):
    for raw_video in os.listdir(f"{video_folder_path}"):
        if(raw_video.endswith(".mkv")):
            if(' ' in raw_video):
                new_name = raw_video.replace(' ', '_')
                os.rename(f"{video_folder_path}\{raw_video}", f"{video_folder_path}\{new_name}")

    print(f"- file names normalization done")