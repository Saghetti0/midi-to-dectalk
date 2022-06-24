# midi-to-dectalk
A tool to convert MIDI files to DECtalk commands. The scripts here were used to create this video: https://www.youtube.com/watch?v=WZIr7cOgWPM

**Caution:** It is incredibly hard to get this to work properly. Making the video above took two people around 15 hours of work to create, and it was an absolute mess. DECtalk is really inconsistent with its timings, so the amount of milliseconds specified in phoneme commands isn't anywhere near accurate to how long DECtalk actually plays it for. We had to heavily edit and stretch a lot of the the audio in order for it to sound correct. Some of it was so broken that we had to resort to using a soundfont. Additionally, the limited pitch range of DECtalk made it difficult to play parts of Megalovania. Notes that are outside of DECtalk's range (higher than C5 or lower than C2) will be clipped to C5 or C2 respectively.

If you need help, feel free to yell at me in my Discord server: https://discord.gg/4kUtKR44nm. My tag is Saghetti#9735, though I'm not accepting friend requests.

## Prerequisites

* Latest python3 installed
* mido and requests for python3 installed
* Ability to understand and edit python code, to fix problems that you may run into

## How to use

1. Create a MIDI file that you want to be converted into DECtalk commands, and save it to the folder.
2. Assign phonemes to MIDI tracks using the `track_phonemes.json` file. NOTE: All tracks that aren't listed in the file, or tracks that have an `_` as their phoneme will be silent! [A full list of phonemes is available here](https://www.digikey.com/htmldatasheets/production/1122220/0/0/1/dectalk-guide.html#pf38)
3. Run `gen.py`, and enter in your MIDI filename. This will output a bunch of files into the `outtext` directory. The file naming is as so: `out_[track]_[voice]_[segment].txt`. The track is the MIDI track number/instrument. Files with the same track and different voice should be played simultaneously in order to get polyphony. DECtalk can't handle large files without crashing, so each voice is split further into segments of 1024 characters. Each segment should be played one after another.
4. Optionally, run `wav_all.py` in order to generate WAV files every file in `outtext`. This uses https://tts.cyzon.us/ in order to generate its files.
5. Before doing another run of `gen.py`, make sure to delete all the files in `outtext` and `outwav`!

There's also a script to generate a soundfont, which is significantly easier.

1. Edit line 4 of `soundfont.py` to contain all the phonemes that you want to generate files for.
2. Run `soundfont.py`, and wait for it to complete.
3. Use the samples in the `soundfont` directory to create the soundfont. It's important to use different samples for each pitch, because just pitch shifting a single sample sounds wrong.

## TODO list

* Add working pitch bends
* Fix timing issues somehow???
