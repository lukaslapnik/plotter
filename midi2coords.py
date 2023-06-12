# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import mido
import math
import numpy as np
import matplotlib.pyplot as plt
import random

midi_file = 'C:/Users/slluka/Documents/Other/Sweden.mid'

def extract_notes(midi_file):
    mid = mido.MidiFile(midi_file)

    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # Default tempo in microseconds per beat (120 BPM)

    notes = []
    time = 0  # Cumulative time in ticks

    for track in mid.tracks:
        for msg in track:
            time += msg.time

            if msg.type == 'set_tempo':
                tempo = msg.tempo

            if msg.type == 'note_on':
                if msg.velocity > 0:
                    note = {
                        'pitch': msg.note,
                        'time': time,
                        'absolute_time': mido.tick2second(time, ticks_per_beat, tempo)  # Convert ticks to absolute time
                    }
                    notes.append(note)

    return notes

# Usage example
notes = extract_notes(midi_file)

for note in notes:
    print(f"Pitch: {note['pitch']}, Time: {note['time']}, Absolute Time: {note['absolute_time']} seconds")

x = []
y = []
coorx = 0
coory = 0
coorxprev = 0
cooryprev = 0
i=0
multiplier = 1
neg = False
first = True
notetimeprev = 17969
angle = 0
size_reduction = 40

x.append(coorx)
y.append(coory)
for note in notes:
    notetime = note['time']
    if notetime != notetimeprev:
        angle = random.uniform(0, 6.28)
        coorx = coorxprev + math.sin(angle) * (notetime-notetimeprev)/size_reduction
        coory = cooryprev + math.cos(angle) * (notetime-notetimeprev)/size_reduction
        x.append(coorx)
        y.append(coory)
        #     first = False
        # else:
        #     x[i] = coorxprev + math.sin(math.radians(note['pitch']))
        #     y[i] = coorxprev + math.cos(math.radians(note['pitch']))
        coorxprev = coorx
        cooryprev = coory
        notetimeprev = notetime
        if neg:
            neg = False
            multiplier = 0.5
        else:
            neg = True
            multiplier = -0.5
    

plt.style.use('_mpl-gallery')
plt.rcParams['figure.dpi'] = 300
#plot
fig, ax = plt.subplots()
   
ax.plot(x, y, linewidth=2.0)

plt.show()