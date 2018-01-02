# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 16:47:02 2017

@author: Nick Butts
"""

import argparse
from audio import clip_record
import os
import matplotlib.pyplot as plt
import numpy as np

def processDictionary(f, data_dir, rate, clipRecorder):
    word = f.readline()
    word = word.strip('\n')
    while word!='':
        word_path = data_dir + word
        if not os.path.exists(word_path):
            os.mkdir(word_path)
        print(word)
        input()
        clipRecorder.recordClip(word)
        audioData = clipRecorder.getAudioAsNp()
        t = np.linspace(0, len(audioData)/rate, len(audioData))
        plt.plot(t, audioData)
        plt.ylim((-32768, 32768))
        plt.title(word)
        plt.show()
        word = f.readline()
        word = word.strip('\n')

def main():
    parser = argparse.ArgumentParser(description='Knox audio capture system')
    parser.add_argument('--rate', '-r', type=int, default=48000, help='the recording rate in Hz')
    parser.add_argument('--user', '-u', type=str, required=True, help='The name of the user recording audio')
    parser.add_argument('--dictionary', '-d', type=str, default='dictionary.txt', help='The list of words and sentences to record')
    parser.add_argument('--duration', type=float, default=2, help='The duration for the recording')
    parser.add_argument('--data_dir', type=str, default='data', help='The location to store the data')

    args = parser.parse_args()
    
    print('Each word will be displayed. Press enter and then say the word')
    print('If you screw up while recording, note which word you made the mistake on')
    
    dd = args.data_dir
    if dd.endswith('/'):        
        dd = dd[0:len(dd)-1]
    
    if not os.path.exists(dd):
        os.mkdir(dd)
        
    dd = dd + '/'
    
    cr = clip_record.ClipRecorder(args.rate, args.user, args.duration, dd)
    
    f = open(args.dictionary, "r")   
    processDictionary(f, dd, args.rate, cr)

if __name__ == "__main__":
    # execute only if run as a script
    main()