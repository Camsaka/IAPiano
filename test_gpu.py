import tensorflow as tf
from tensorflow.python.client import device_lib

config = tf.ConfigProto( device_count = {'GPU': 0 , 'CPU': 2} ) 
sess = tf.Session(config=config) 
keras.backend.set_session(sess)
print(device_lib.list_local_devices())
print(tf.debugging.set_log_device_placement(True))