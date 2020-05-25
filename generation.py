from music21 import converter, instrument, note, chord, stream
import glob
import numpy as np
import pickle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import BatchNormalization as BatchNorm
from keras.callbacks import ModelCheckpoint

import mido
import rtmidi
import time
import random
from random import uniform

def prepare_sequences(notes,n_vocab,pitches):
	#récupération de tous les pitch du fichier
	pitchnames = sorted(set(item for item in notes))
	# print(pitchnames)

	# Création d'un dictionnaire (facilite la manipulation) index:note/chord value:int 0-153
	note_dict = dict((note, nb) for nb, note in enumerate(pitches))
	network_input = []
	network_output = []
	# print(note_to_int)


	# sequence_length défini le nombre de notes dans chaque sequence
	# paramètres influent sur le calcul, à tester avec différentes valeurs
	sequence_length=50

	# creation des sequences d'entrée du RNN et des sorties correspondantes
	# input: sequence de note de longueur sequence_length, output : la note suivant la sequence

	# print(len(notes))
	for i in range(0, len(notes) - sequence_length, 1):
	    sequence_in = notes[i:i + sequence_length]
	    # print(sequence_in)
	    # print(len(sequence_in))
	    sequence_out = notes[i + sequence_length]
	    network_input.append([note_dict[char] for char in sequence_in])
	    # print(network_input)
	    # print("\n")
	    network_output.append(note_dict[sequence_out])
	    n_patterns = len(network_input)

	# reshape de l'input dans un format matricielle lisible par le RNN LSTM
	# set(list) retourne le nombre d'éléments uniques d'une list
	n_vocab = len(set(notes))
	network_input = np.reshape(network_input, (n_patterns, sequence_length,1)) #----------------- attention 3D possible 3e dim = 1??
	# normalisation, gros chiffres moins bien traités pas les RNN LSTM
	network_input = network_input / float(n_vocab)
	# print(network_input[2])

	# one_hot_encoding 
	network_output = np_utils.to_categorical(network_output)

	return(network_input,network_output)


def create_model(network_input,n_vocab):
	model = Sequential()
	model.add(LSTM(
	50,
	input_shape=(network_input.shape[1], network_input.shape[2]),
	return_sequences=True
	))
	model.add(Dropout(0.3))
	model.add(LSTM(100, return_sequences=True))
	model.add(Dropout(0.3))
	model.add(LSTM(100))
	model.add(Dense(50))
	model.add(Dropout(0.3))
	model.add(Dense(n_vocab))
	model.add(Activation('softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')

	# Load the weights to each node
	model.load_weights('weights_tests/weights-sequence50_700_loss-1.91_Adam.hdf5')

	return model

# back to music21

def generate_notes(modele, inN, pitches, n_vocab):
	int_to_note = dict((nb, note) for nb, note in enumerate(pitches))
	start = np.random.randint(0, len(inN)-1)
	sequence = inN[start]
	prediction_output = []
	# générer 100 notes
	for nb_note in range(50):
		prediction_input= np.reshape(sequence, (1, len(sequence), 1))
		prediction = modele.predict(prediction_input)
		# print("prediction")
		# print(prediction)
		# prediction = np.random.rand(100)
		# print("iteration:"+str(nb_note)+"start:"+str(start))
		# print(prediction_input)
		index = np.argmax(prediction)
		# print("index argmax")
		# print(index)
		result = int_to_note[index]
		# print("result"+str(result))
		prediction_output.append(result)
		sequence = np.append(sequence,prediction[0][index])
		sequence = sequence[1:len(sequence)]
		# print(sequence)
		print(prediction_output)
	return prediction_output



def generate():
	with open('notes_mem', 'rb') as filepath:
		notes = pickle.load(filepath)
	# print(notes)
	pitches = sorted(set(item for item in notes))
	# print(pitches)
	n_vocab = len(set(notes))
	inN,outN = prepare_sequences(notes,n_vocab,pitches)
	modele = create_model(inN,n_vocab)
	seq = generate_notes(modele,inN,pitches,n_vocab)
	return seq



def convert_midi(prediction):

    offset = 0
    output_notes = []

    for pattern in prediction:
        # pattern est un accord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern est une note note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        
        offset += 0.6

        # ajout d'off-set pour faire avancer les notes dans le temps
        

    midi_stream = stream.Stream(output_notes)

    midi_stream.write('midi', fp='test_output.mid')#Modifier le nom du fichier midi ici.

seq = generate()
# print(seq)
mid = convert_midi(seq)