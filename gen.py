from time import time
import mido
import math
import json

with open("track_phonemes.json", "r") as fh:
    track_phonemes = json.loads(fh.read())

def midi_to_dectalk(note_value):
    #return math.floor(440 * pow(2, (note_value-69)/12))

    if note_value < 37: # 37 = c2 in midi
        return 1
    if note_value > 72: # 72 = c5 in midi
        return 37
    return note_value - 35

class DectalkVoice:
    def __init__(self, voice_id, sound_to_use):
        self.stream = []
        self.playing_note = False
        self.current_note_value = 0
        self.last_timestamp = 0
        self.sound_to_use = sound_to_use
        self.voice_id = voice_id

    def note_on(self, midi_note_value, timestamp):
        if self.playing_note:
            raise Exception("already playing note??? wtf")
        
        self.playing_note = True
        self.current_note_value = midi_note_value
        if (timestamp - self.last_timestamp) > 0:
            self.stream.append(f"_<{math.floor(timestamp - self.last_timestamp)}>")
        self.last_timestamp = timestamp
    
    def note_off(self, timestamp):
        if not self.playing_note:
            raise Exception("not playing note??? wtf")
        
        self.playing_note = False
        if (timestamp - self.last_timestamp) > 0:
            self.stream.append(f"{self.sound_to_use}<{math.floor(timestamp - self.last_timestamp)},{midi_to_dectalk(self.current_note_value)}>")
        self.last_timestamp = timestamp

mid = mido.MidiFile(input("file: "), clip=True)

track_id = 0

print(mid.type)

tempo = 500000

for track in mid.tracks:
    print("Processing track", track_id)

    ms_counter = 0
    voices = [DectalkVoice(i, track_phonemes.get(str(track_id), "_")) for i in range(8)]
    note_voice_map = {}

    for msg in mid.tracks[track_id]:
        if msg.time > 0:
            ms_counter += mido.tick2second(msg.time, mid.ticks_per_beat, tempo) * 1000
        
        #print(ms_counter, msg)

        if msg.type == "set_tempo":
            print(f"Tempo={msg.tempo}")
            tempo = msg.tempo
            print(f"BPM={mido.tempo2bpm(tempo)}")
            print(f"Ticks/beat={mid.ticks_per_beat}")
        elif msg.type == "end_of_track":
            print("End of track", track_id)
            for voice in voices:
                if voice.playing_note:
                    voice.note_off(ms_counter)
            print("Stream items per voice: ", end="")
            for voice in voices:
                print(f"{len(voice.stream)}, ", end="")
            print()
            break
        elif msg.type == "note_on":
            selected_voice = None
            
            for voice in voices:
                if not voice.playing_note:
                    selected_voice = voice
                    break
            
            if selected_voice == None:
                raise Exception(f"ran out of voices?? ms_counter={ms_counter}")

            selected_voice.note_on(msg.note, ms_counter)
            if note_voice_map.get(msg.note) is None:
                note_voice_map[msg.note] = []

            note_voice_map[msg.note].append(selected_voice)
        elif msg.type == "note_off":
            selected_voice_list = note_voice_map.get(msg.note)

            if selected_voice_list == None:
                raise Exception(f"couldn't find voice list?? msg.note={msg.note} ms_counter={ms_counter} note_voice_map={note_voice_map}")

            if len(selected_voice_list) == 0:
                raise Exception(f"voice list is empty?? msg.note={msg.note} ms_counter={ms_counter} note_voice_map={note_voice_map}")

            selected_voice = selected_voice_list.pop(0)
            selected_voice.note_off(ms_counter)

            if len(selected_voice_list) == 0:
                del note_voice_map[msg.note]
    
    for voice in voices:
        file_ctr = 0
        while len(voice.stream) > 0:
            with open(f"outtext/out_{track_id}_{voice.voice_id}_{file_ctr}.txt", "w") as fh:
                fh.write("[:phoneme on] [:rate 600] [")

                while (fh.tell() < 1000) and (len(voice.stream) > 0):
                    fh.write(voice.stream.pop(0))
                
                fh.write("]")
            file_ctr += 1

    track_id += 1   