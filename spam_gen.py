import numpy as np, sys, tensorflow as tf
import tflearn
from keras.utils import np_utils

fname = sys.argv[1]
input = open(fname).read().lower()
chars = sorted(list(set(input)))
charint = dict((char,ints) for ints, char in enumerate(chars))
intchar = dict((ints, char) for ints, char in enumerate(chars))
outname = fname + "_gen"
seqlen = 100
lstmhid=320
keeprate = 0.8
train = []
true = []

tf.reset_default_graph()

for i in range(0, len(input)-seqlen, 1):
    train.append([charint[char] for char in input[i:i+seqlen]])
    true.append(charint[input[i+seqlen]])

x = np.reshape(train, (len(train), seqlen, 1))/float(len(chars)) 
y = np_utils.to_categorical(true)
net = tflearn.input_data(shape=(None, x.shape[1], x.shape[2]))
net = tflearn.lstm(net, lstmhid)
net = tflearn.regression(net, optimizer='adam', learning_rate=0.005, loss='categorical_crossentropy')
model = tflearn.DNN(net, checkpoint_path = 'charmodel/model.tfl.ckpt')
model.fit(x, y, snapshot_epoch=True, snapshot_step=5000, n_epoch=20, batch_size = 128)
model.save(outname)
