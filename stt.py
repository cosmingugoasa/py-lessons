import speech_recognition as sr 
import pyttsx3
import sys

#################################################
#   RECOG FUNCTION
#################################################
def recog(audioFile, recogInstance, count, audio_chunks, stt_chunks):
    with audioFile as source:
        recogInstance.pause_threshold = 90
        audio = recogInstance.listen(source)                        
       
        try:
            stt_chunk = recogInstance.recognize_google(audio, language="it-IT")
            stt_chunk = stt_chunk.lower()
            #stt_chunks.append(stt_chunk)
            stt_chunks[count] = stt_chunk
            #print(f"** Elaborazione : {count}**")
        except Exception as e:
            print(f"**[CHUNK : {count}] Could not understand audio. {e}**")