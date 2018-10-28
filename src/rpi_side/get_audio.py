#coding:utf-8

import pyaudio
import threading
import numpy as np
from pathlib import Path
from take_picture import AutoTakePictures
#from matplotlib import pyplot as plt

chunk = 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1

STOCK_FILE_NUM = 20

p = pyaudio.PyAudio()
picture = AutoTakePictures()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = chunk,
)

max_data = []
def audio_trans(input):
    frames = (np.frombuffer(input,dtype="int16"))
    max_data.append(max(frames))
    return max_data

# callback per term
def sendlog():
    global max_data

    if len(max_data) != 0:
        #print(max_data)
        mic_mean = int(sum(max_data)/len(max_data))
        max_data = []
        print(mic_mean)
        # over level 15000
        if mic_mean > 15000:
            picture.capture()
        file_numbers = list(Path(picture.save_dir).glob("*.jpg")).__len__()
        if file_numbers >= STOCK_FILE_NUM:
            picture.sendServer(server="18.191.254.247",user="ec2-user",key="jphack2018-01.pem")
            picture.delete()
            
    # thread per 1
    t = threading.Timer(1,sendlog)
    t.start()
    
# thread
t = threading.Thread(target = sendlog)
t.start()
    
while stream.is_active():
    input = stream.read(chunk)
    input = audio_trans(input)

stream.stop_stream()
stream.close()
p.terminate()

