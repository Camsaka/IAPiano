import mido
import rtmidi
import time
import random


print("Bonjour")

# on affiche les sortie possibles
print(mido.get_output_names())

# MIDI-OUT redirigera tout vers cest port 
outport = mido.open_output('FLUID Synth (1918):Synth input port (1918:0) 128:0')
# outport = mido.open_output('VMPK Input:VMPK Input 130:0')

# outport.send(mido.Message('note_on', channel=3, note=60, velocity=100))
# outport.send(mido.Message('note_off', channel=3, note=60))
# time.sleep(1)

# outport.send(mido.Message('note_on', channel=3, note=60, velocity=100))
# outport.send(mido.Message('note_off', channel=3, note=60))
# time.sleep(1)

# i = 34  # initialisation variable i pour note 24 = Do1
# ch=9
# while i<100:  # boucle notes à jouer dans la gamme Chromatique 24 à 96 / Do1 à Do7
# 	outport.send(mido.Message('program_change', channel=ch, program = i)) # canal/programme
# 	print("Note =", i)  # affiche numéro de note jouée
# 	outport.send(mido.Message('note_on', channel = ch, note=i, velocity=100))
# 	time.sleep(1)  # durée d'environ 1/3 seconde
# 	outport.send(mido.Message('note_off', channel=ch, note=i))
# 	i = i + 1  # incrémentation de l'index i (note jouée)




# i = 0   # 1) variable i=0 pour instrument Up (ou i=127 pour Down)
# ch = 1  # variable ch=0 à 15 choix du canal Midi - ici 1 correspond au canal 2 Qsynth
# while i<128:  # 2) boucle accord Do3 pour les 128 instruments GM avec i<128 (ou i>=0)
#     alea = random.randrange(1,4) # générateur valeurs aléatoires entre 1 et 3
#     print("=> Instrument #",i,"- Canal #",ch, end="  ") # instrument GM 0...127 + durée aléatoire
#     outport.send(mido.Message('program_change', channel=ch, program=i)) # canal/programme
#     outport.send(mido.Message('note_on', channel=ch, note=48, velocity=90))
#     time.sleep(alea *0.2)  # durée aléatoire pondérée pour donner semblant de vie
#     outport.send(mido.Message('note_off', channel=ch, note=48))
#     outport.send(mido.Message('note_on', channel=ch, note=52, velocity=102))
#     time.sleep(alea *0.1)  # durée aléatoire...
#     outport.send(mido.Message('note_off', channel=ch, note=52))
#     outport.send(mido.Message('note_on', channel=ch, note=55, velocity=114))
#     time.sleep(alea *0.1)  # durée aléatoire...
#     outport.send(mido.Message('note_off', channel=ch, note=55))
#     outport.send(mido.Message('note_on', channel=ch, note=60, velocity=127))
#     time.sleep(alea *0.3)  # durée aléatoire de 0.3, 0.6 ou 0.9 seconde
#     outport.send(mido.Message('note_off', channel=ch, note=60))
#     print("suivant...")
#     i = i +1  # 3) up +1 (ou down -1) du compteur i - voir ci-dessus 1) & 2)
# print("TERMINÉ !")



mid = mido.MidiFile('test_output.mid')
for msg in mid.play():
    outport.send(msg)

