# breakcoreify

Turns any song into endless breakcore.

## Dependencies

* Python 3.x
* FFmpeg
* NumPy

## Usage

```bash
python3 breakcoreify.py --in=INPUT_FILE.mp3 --out=OUTPUT_FILE.mp3 [--backing=BACKING_FILE.mp3] [--changes=INT] [--phrase-length=INT]
```

* --in=INPUT_FILE.mp3: Any local song in audio form that you want to convert into breakcore.
* --out=OUTPUT_FILE.mp3: The outputted audio file path.
* --backing=BACKING_FILE.mp3: The track to be played on loop throughout the song (usually drums) (OPTIONAL, recommend "amen-break.mp3").
* --changes=INT: The total number of times that the song alters itself (OPTIONAL).
* --phrase-length=INT: The number of loops it takes before a song alteration happens (OPTIONAL).

## Disclaimer

This is a simple script, initially written in a couple of hours, and as such, the breakcore that one may hear might not be an accurate or high-quality representation of what breakcore is like. My goal was only for it to at least be halfway listenable as background music, for studying and such.
