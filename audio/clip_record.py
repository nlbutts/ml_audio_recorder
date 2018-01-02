# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyaudio
import wave
import glob 
import re
import numpy as np
import struct

class ClipRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"

    def __init__(self, rate, user, duration, data_dir):
        self.RATE = rate
        self.USER = user
        self.audio = pyaudio.PyAudio()
        self.DURATION = duration
        self.DATA_DIR = data_dir
        print(self.audio.get_default_input_device_info())
        self.AUDIO_DATA = []
        
    def recordClip(self, label):
        # start Recording
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        print("recording... {0}".format(label))
        frames = []
         
        for i in range(0, int(self.RATE / self.CHUNK * self.DURATION)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        #print("finished recording")
                 
        # stop Recording
        stream.stop_stream()
        stream.close()

        self.AUDIO_DATA = frames
                
        searchPath = self.DATA_DIR + label + '/' + self.USER + '_nohash*'
        files = glob.glob(searchPath)
        count = 0
        l = len(files)
        if l > 0:            
            files = sorted(files)
            m = re.search('.*_nohash_(.*).wav', files[l-1])
            count = int(m.group(1))
            count += 1
        outputFile = self.DATA_DIR  + label + '/' + self.USER + '_nohash'
        countStr = '{0:02}'.format(count)
        outputFile = outputFile + '_' + countStr + '.wav'
        print('saving to {0}'.format(outputFile))

        waveFile = wave.open(outputFile, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
    def getAudio(self):
        return self.AUDIO_DATA
    
    def getAudioAsNp(self):
        data=[]
        for x in self.AUDIO_DATA:
            for i in range(len(x)//2):
                y = x[i*2:(i*2)+2]
                z = struct.unpack('<h', y)
                data.append(z[0])
        return np.array(data)                