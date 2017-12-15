import numpy as np, tflearn, sys, tensorflow as tf
from keras.utils import np_utils

#input file, .txt file to be used as training data
input = open(sys.argv[1]).read().lower()
#turn everything into char array
chars = sorted(list(set(input)))
#create integer dictionary from character (converting characters to number values)
charint = dict((char,ints) for ints, char in enumerate(chars))
intchar = dict((ints,char) for ints, char in enumerate(chars))

#parsing input (model name)
ff = sys.argv[1][:-4]
f = ff.split("/")
#output name for the model
filename = f[2]
print("Analyzing:", filename)

#number of characters per analysis
seqlen = 100
#long short term memory value (how much memory retained by the RNN) //double check
lstmhid=320
#how much information info retained per iteration
keeprate = 0.80
#train set
train = []
true = []
#initialize tf stuff
tf.reset_default_graph()
#create training set of seqlen long character chunks
for i in range(0, len(input)-seqlen, 1):
    train.append([charint[char] for char in input[i:i+seqlen]])
    true.append(charint[input[i+seqlen]])
#tensor stuff/learning
X = np.reshape(train, (len(train), seqlen, 1))/float(len(chars))
y = np_utils.to_categorical(true)
net = tflearn.input_data(shape=(None, X.shape[1], X.shape[2]))
net = tflearn.lstm(net, lstmhid)
net = tflearn.fully_connected(net, y.shape[1], activation='softmax')
net = tflearn.regression(net, optimizer='adam',
 learning_rate=0.005, loss ='categorical_crossentropy')
#creates the container for the model
model = tflearn.DNN(net, checkpoint_path = 'charmodel/model.tfl.ckpt')
#actually create the model (comment this line out when generating
model.fit(X, y, snapshot_epoch=True, snapshot_step=5000, n_epoch=20, batch_size = 250)
#save the model (comment this line out when generating
model.save(filename)
#all this code should be uncommented to generate output
#model.load(filename)
#chooses random training sample and outputs model's generation from that
#for _ in range(5):
#    p = train[np.random.randint(0,len(train)-1)]
#    print("Seed:")
#    print("\"",''.join([intchar[value] for value in p]), "\"")
#    print("/////////")
#    for _ in range(100):
#        sys.stdout.write((intchar[np.argmax(model.predict((np.reshape(p, (1, len(p), 1))/float(len(chars)))))]))
#    p.append(np.argmax(model.predict((np.reshape(p, (1, len(p), 1))/float(len(chars))))))
#    p = p[1:len(p)]
#    print("\n============================\n")
