#!/usr/bin/env python3

import random
import numpy as np
import os
import sys

def randomPattern():
    positions = [random.random() for i in range(8)]

    types = [
        [(0, 1), (1, 1), (2, 1), (3, 1)] * 2,
        ([(0, 1), (1, 1), (2, 1)] * 2) + [(0, 1), (1, 1)],
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 1), (1, 1), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
        [(0, 1), (1, 2), (0, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 2), (0, 1), (1, 2), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (3, 2), (0, 1), (3, 2)],
        [(0, 8)],
        [(0, 4), (1, 4)],
        [(0, 4), (0, 4)],
        [(0, 2)] * 4,
        [(0, 1)] * 8,
    ]

    ret = []
    type2 = random.choice(types)

    for value in type2:
        ret.append((positions[value[0]], value[1]))

    return ret

def getClip(pattern, path, backingSize):
    maxSize = os.path.getsize(path)

    output = np.array([])
    rate = int(backingSize / 4)
    rate -= rate % 2

    with open(path, 'rb') as f:
        for p in pattern:
            size = p[1] * rate
            index = int(p[0] * (maxSize - size))
            index -= index % 2

            f.seek(index)
            part = np.frombuffer(f.read(size), dtype=np.int16).astype(np.float32)

            output = np.append(output, part)

    return output

def infiniteProgression(path, outputPath, measuresPerPattern, numIters, backing=None):
    if backing == None:
        backingClip = getClip(randomPattern(), path, 176400)
    else:
        with open(backing, 'rb') as f:
            backingClip = np.frombuffer(f.read(), dtype=np.int16).astype(np.float32)

    current = np.zeros(len(backingClip))

    for i in range(numIters):
        print(f'Progress: {i} / {numIters}')

        current += getClip(randomPattern(), path, len(backingClip))

        if max(abs(current)) > 0:
            current *= max(abs(backingClip)) / max(abs(current))
            current *= 0.7

        for j in range(measuresPerPattern):
            exportClip(current + backingClip, outputPath, append=(i > 0))

def exportClip(clip, path, append=False):
    with open(path, 'ab' if append else 'wb') as f:
        f.write((clip / 10).astype(np.int16).tobytes())

def playClip(clip):
    exportClip(clip)
    os.system('paplay --raw --rate 44100 --channels 2 output.pcm')

def main():
    backingFile = None
    inputFile = None
    outputFile = None
    changes = 64
    phraseLength = 16

    printHelp = False

    argCount = 0

    for arg in sys.argv[1 :]:
        if arg.startswith('--in='):
            inputFile = arg.removeprefix('--in=')
        elif arg.startswith('--out='):
            outputFile = arg.removeprefix('--out=')
        elif arg.startswith('--backing='):
            backingFile = arg.removeprefix('--backing=')
        elif arg.startswith('--changes='):
            try:
                changes = int(arg.removeprefix('--changes='))
            except ValueError:
                print('Not an int: ' + arg.removeprefix('--changes='))
                printHelp = True
                break
        elif arg.startswith('--phrase-length='):
            try:
                phraseLength = int(arg.removeprefix('--phrase-length='))
            except ValueError:
                print('Not an int: ' + arg.removeprefix('--phrase-length='))
                printHelp = True
                break
        else:
            print('Invalid arg: ' + arg)
            printHelp = True
            break

    if not printHelp and inputFile == None:
        print('Missing argument: --in=INPUT_FILE')
        printHelp = True

    if not printHelp and outputFile == None:
        print('Missing argument: --out=OUTPUT_FILE')
        printHelp = True

    if not printHelp and not os.path.exists(inputFile):
        print('File does not exist: ' + inputFile)
        printHelp = True

    if not printHelp and backingFile != None and not os.path.exists(backingFile):
        print('File does not exist: ' + backingFile)
        printHelp = True

    if printHelp:
        print('Syntax: breakcoreify.py --in=INPUT_FILE.mp3 --out=OUTPUT_FILE.mp3 [--backing=BACKING_FILE.pcm] [--changes=INT] [--phrase-length=INT]')
        return
    
    os.system(f'ffmpeg -y -i "{inputFile}" -ar 44100 -ac 2 -sample_fmt s16 -f s16le "{inputFile}.pcm"')
    os.system(f'ffmpeg -y -i "{backingFile}" -ar 44100 -ac 2 -sample_fmt s16 -f s16le "{backingFile}.pcm"')
    infiniteProgression(inputFile + '.pcm', outputFile + '.pcm', phraseLength, changes, backingFile if backingFile == None else backingFile + '.pcm')
    os.system(f'ffmpeg -y -ar 44100 -ac 2 -sample_fmt s16 -f s16le -i "{outputFile}.pcm" "{outputFile}"')

    for path in [inputFile + '.pcm', outputFile + '.pcm', backingFile + '.pcm']:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    main()
