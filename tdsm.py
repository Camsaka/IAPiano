from music21 import converter, instrument, note, chord
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

def get_notes():
	notes = []
	leng = 0 
	for file in glob.glob("data_midi/*.mid"):
	    midi = converter.parse(file)
	    notes_trad = None

	    parties = instrument.partitionByInstrument(midi) #classe les signaux par instruments dans des objets, ici nous n'avons que du piano
	    # parties.show('text')

	    leng=leng+1
	    # print(leng)#doit etre egal au nombre de fichier midi si on ne joue qu'un seul instrument
	    # afficher les objets instruments (ici un piano pour chaque fichier midi)


	    if parties: # instrument
	        notes_trad = parties.parts[0].recurse()
	        # print(notes_trad)
	    else: # non precisé (flat) (facultatif si on est sur de n'avoir des signaux destiné à un instrument)
	        notes_trad = midi.flat.notes
	        # print("flat")
	        # print(notes_trad)


	    for element in notes_trad:
	        if isinstance(element, note.Note):
	        	print(element.pitch)
	        	notes.append(str(element.pitch))
	        elif isinstance(element, chord.Chord):
	            notes.append('.'.join(str(n) for n in element.normalOrder)) #traduit l'accord en une chaine d'entiers (notes ordres standard)

	# sauvegarde des notes utilisées à l'entrainement, servira pour la generation des fichiers midi (generation.py)
	# wb pour l'ouvrir en ecriture et binaire(pour se servir de pickle)
	with open('notes_mem', 'wb') as filepath:
		pickle.dump(notes, filepath)
	return notes

# notes = get_notes();
# print(notes)
# print(len(notes))

def prepare_sequences(notes,n_vocab):
	#récupération de tous les pitch du fichier
	pitchnames = sorted(set(item for item in notes))
	# print(pitchnames)

	# Création d'un dictionnaire (facilite la manipulation) index:note/chord value:int 0-153
	note_dict = dict((note, nb) for nb, note in enumerate(pitchnames))
	network_input = []
	network_output = []
	# print(note_to_int)


	# sequence_length défini le nombre de notes dans chaque sequence
	# paramètres influent sur le calcul, à tester avec différentes valeurs
	sequence_length=50

	# creation des sequences d'entrée du RNN et des sorties correspondantes
	# input: sequence de note de longueur sequence_length, output : la note suivant la sequence

	# print(len(notes))
	for i in range(0, len(notes) - sequence_length,1):
	    sequence_in = notes[i:i + sequence_length]
	    # print(sequence_in)
	    # print(len(sequence_in))
	    sequence_out = notes[i + sequence_length]
	    network_input.append([note_dict[char] for char in sequence_in])
	    # print(network_input)
	    # print("\n")
	    network_output.append(note_dict[sequence_out])

	n_patterns = len(network_input)
	print(len(network_input))
	print(len(network_output))

	# reshape de l'input dans un format matricielle lisible par le RNN LSTM
	# set(list) retourne le nombre d'éléments uniques d'une list
	network_input = np.reshape(network_input, (n_patterns, sequence_length,1)) #----------------- attention 3D possible 3e dim = 1??
	# normalisation, gros chiffres moins bien traités pas les RNN LSTM
	network_input = network_input / float(n_vocab)

	# one_hot_encoding 
	network_output = np_utils.to_categorical(network_output)

	return(network_input,network_output)

# prepare_sequences(notes,len(set(notes)))

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
# optimizer : rmsprop,adam
	return model

def training(network_input,network_output,modele):

	# CheckPoint with Keras
	# Permet a chaque iteration d'enregistrer le vecteur de poids
	# Pas de perte en cas d'arret du script, a l'inverse on devrait attendre la fin de tous les epochs pour sauvegarder nos resultats

	# filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
	filepath = "weights.hdf5"
	checkpoint = ModelCheckpoint(
    filepath, monitor='loss', 
    verbose=0,
    save_best_only=True,        
    mode='min'
)    
	callback = [checkpoint]     

	# fit  pour entrainer le modele keras
	modele.fit(network_input, network_output, epochs=500, batch_size=64, callbacks=callback)



def train():
	notes = get_notes()
	n=len(set(notes))
	inN,outN = prepare_sequences(notes,n)
	modele = create_model(inN,n)
	training(inN,outN,modele) 


train()