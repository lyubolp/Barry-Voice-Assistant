import subprocess
import sys
import os

text = sys.argv[1]
isOutputWavFile = 0
pathToWav = ''

if len(sys.argv) == 4:
    isOutputWavFile = sys.argv[2]
    pathToWav = sys.argv[3]

mimic_command = './mimic1/mimic -t "' + text + '" -voice ./mimic1/voices/new_voice.flitevox'

if isOutputWavFile == '1':
    mimic_command += ' -o '
    mimic_command += pathToWav

print(mimic_command)
os.system(mimic_command)
