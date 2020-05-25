import mido
import rtmidi
import time

# on affiche les sortie possibles
print(mido.get_output_names())

# MIDI-OUT redirigera tout vers ce port 
outport = mido.open_output('FLUID Synth (24939):Synth input port (24939:0) 128:0') #Remplacer ici

mid = mido.MidiFile('test_output.mid')
for msg in mid.play():
    outport.send(msg)

