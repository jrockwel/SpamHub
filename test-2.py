import numpy as np, tflearn, sys, tensorflow as tf
from keras.utils import np_utils

#open .txt file to use as training data
input = open("spam_poetry.txt").read().lower()
#create array of ordered characters from input file
chars = sorted(list(set(input)))
#convert characters to integer values and put into dictionary for training
charint = dict((char,ints) for ints, char in enumerate(chars))
intchar = dict((ints,char) for ints, char in enumerate(chars))
#create outputfile
filename = 'spam_out.txt'

#figure out what this is=len of info to retain/len of text sequence to learn
seqlen = 100
#number of units for RNN [long-short term memory]
lstmhid=320
#amount to retain in learning (re: RNNs)
keeprate = 0.80
train = []
true = []
tf.reset_default_graph()
#add characters to training set
for i in range(0, len(input)-seqlen, 1):
    train.append([charint[char] for char in input[i:i+seqlen]])
    true.append(charint[input[i+seqlen]])
#format training array
X = np.reshape(train, (len(train), seqlen, 1))/float(len(chars))
y = np_utils.to_categorical(true)
#create RNN
net = tflearn.input_data(shape=(None, X.shape[1], X.shape[2]))
net = tflearn.lstm(net, lstmhid)
net = tflearn.fully_connected(net, y.shape[1], activation='softmax')
net = tflearn.regression(net, optimizer='adam',
 learning_rate=0.005, loss ='categorical_crossentropy')
#use model to generate?/params for how long to run
model = tflearn.DNN(net, checkpoint_path = 'charmodel/model.tfl.ckpt')
model.fit(X, y, snapshot_epoch=True,
snapshot_step=5000, n_epoch=5, batch_size = 50)
#save output
model.save(filename)
