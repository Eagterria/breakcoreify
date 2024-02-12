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

def getClip(pattern, path, backing):
    maxSize = os.path.getsize(path)

    output = np.array([])
    rate = int(os.path.getsize(backing) / 8)
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

def infiniteProgression(path, measuresPerPattern, numIters, backing):
    current = np.zeros(len(getClip(randomPattern(), path, backing)))

    with open(backing, 'rb') as f:
        backingClip = np.frombuffer(f.read(), dtype=np.int16).astype(np.float32)

    backingClipLoop = backingClip

    while len(backingClipLoop) < len(current):
        backingClipLoop = np.append(backingClipLoop, backingClip)

    backingClipLoop = backingClipLoop[: len(current)]

    for i in range(numIters):
        print(f'Progress: {i} / {numIters}')

        current += getClip(randomPattern(), path, backing)

        if max(abs(current)) > 0:
            current *= max(abs(backingClipLoop)) / max(abs(current))
            current *= 0.7

        for j in range(measuresPerPattern):
            exportClip(current + backingClipLoop, append=True)

def exportClip(clip, append=False):
    with open('output.pcm', 'ab' if append else 'wb') as f:
        f.write((clip / 10).astype(np.int16).tobytes())

def playClip(clip):
    exportClip(clip)
    os.system('paplay --raw --rate 44100 --channels 2 output.pcm')

def main():
    os.system(f'ffmpeg -y -i "{sys.argv[1]}" -ar 44100 -ac 2 -sample_fmt s16 -f s16le "{sys.argv[1]}.pcm"')
    infiniteProgression(sys.argv[1] + '.pcm', 16, 64, 'amen-break.pcm')
    os.system(f'ffmpeg -y -ar 44100 -ac 2 -sample_fmt s16 -f s16le -i output.pcm "{sys.argv[2]}"')
    os.system(f'rm "{sys.argv[1]}.pcm" output.pcm')

if __name__ == '__main__':
    main()
