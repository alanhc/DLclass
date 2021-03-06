# -*- coding: utf-8 -*-
"""week6_class-KL_loss_func.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lj-U34p9RLUPJsbGN47y0Xcf2BrbPO81
"""

from google.colab import drive
drive.mount('/content/drive')
import os
os.chdir('/content/drive/My Drive/dataset')

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
import tensorflow
print(tensorflow.__version__)

# updating using keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils
import keras.callbacks as cb
class LossHistory(cb.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        batch_loss = logs.get('loss')
        self.losses.append(batch_loss)

def plot_losses(history):
    plt.figure(1, figsize=(10,10)) 
    plt.subplot(211)   # 2 by 1 array of subplots, and draw the first one 
    plt.plot(history['loss'])   
    plt.title('model loss')  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train'], loc='upper right')
	
    plt.subplot(212)   # 2 by 1 array of subplots, and draw the second one 
    plt.plot(history['acc'])  
    plt.title('model accuracy')  
    plt.ylabel('acc')  
    plt.xlabel('epoch')  
    plt.legend(['train'], loc='lower right')  
	
    plt.show()   

class Solution():
  def __init__(self,X_train,y_train, X_test, y_test):
    #shape = y_train.shape
    #(self.rows,self.c) = shape
    #y_train = np_utils.to_categorical(y_train, self.rows)

    self.X_train = X_train
    self.y_train = y_train
    self.X_test = X_test
    self.y_test = y_test
    #print('X_train:\n',self.X_train) #debug
    print('train X shape',self.X_train.shape) #debug
    #print('Y_train:\n',self.y_train) #debug
    print('train Y shape',self.y_train.shape) #debug

  def init_model(self):
    model = Sequential()
    model.add(Dense(100, input_dim=8))
    model.add(Activation('relu'))
    

    model.add(Dense(1))
    model.add(Activation('relu'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    self.model = model
    return model
  
  def run_network(self, epochs=20, batch=1):
    try:
      if self.model is None:
            self.model = init_model()
      history = LossHistory()
      history = self.model.fit( 
                                self.X_train, self.y_train,
                                epochs=epochs,batch_size=batch,
                                callbacks=[history],
                                verbose=1
                               )
      loss, acc =self.model.evaluate(self.X_train, self.y_train) #加這行評估模型
      print(acc)
      return history.history

    except KeyboardInterrupt:
        print (' KeyboardInterrupt')
        return model, history.losses

import numpy as np
from matplotlib import pyplot as plt

pima = np.loadtxt('./pima-indians-diabetes.data',delimiter=',')

# Various preprocessing steps
pima[np.where(pima[:,0]>8),0] = 8

pima[np.where(pima[:,7]<=30),7] = 1
pima[np.where((pima[:,7]>30) & (pima[:,7]<=40)),7] = 2
pima[np.where((pima[:,7]>40) & (pima[:,7]<=50)),7] = 3
pima[np.where((pima[:,7]>50) & (pima[:,7]<=60)),7] = 4
pima[np.where(pima[:,7]>60),7] = 5

pima[:,:8] = pima[:,:8]-pima[:,:8].mean(axis=0)
pima[:,:8] = pima[:,:8]/pima[:,:8].var(axis=0)

trainin = pima[::2,:8]
testin = pima[1::2,:8]
traintgt = pima[::2,8:9]
testtgt = pima[1::2,8:9]
print(trainin.shape)
print(testin.shape)
print(traintgt.shape)
print(testtgt.shape)

pima_solution = Solution(trainin,traintgt,testin,testtgt)

pima_solution.init_model()
import time
start_time = time.time()
history = pima_solution.run_network(epochs=20, batch=1)
print("--- %s seconds ---" % (time.time() - start_time))
#print(losses)
plot_losses(history)

"""# pima_new_kullback_leibler_divergence.py: 新loss 函式的版本"""

# updating using keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils
import keras.callbacks as cb
from keras.utils import to_categorical
class LossHistory(cb.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        batch_loss = logs.get('loss')
        self.losses.append(batch_loss)

def plot_losses(history):
    plt.figure(1, figsize=(10,10)) 
    plt.subplot(211)   # 2 by 1 array of subplots, and draw the first one 
    plt.plot(history['loss'])   
    plt.title('model loss')  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train'], loc='upper right')
	
    plt.subplot(212)   # 2 by 1 array of subplots, and draw the second one 
    plt.plot(history['acc'])  
    plt.title('model accuracy')  
    plt.ylabel('acc')  
    plt.xlabel('epoch')  
    plt.legend(['train'], loc='lower right')  
	
    plt.show()   

class Solution():
  def __init__(self,X_train,y_train, X_test, y_test):
    #shape = y_train.shape
    #(self.rows,self.c) = shape
    #y_train = np_utils.to_categorical(y_train, self.rows)

    self.X_train = X_train
    self.y_train = y_train
    self.X_test = X_test
    self.y_test = y_test
    #print('X_train:\n',self.X_train) #debug
    print('train X shape',self.X_train.shape) #debug
    #print('Y_train:\n',self.y_train) #debug
    print('train Y shape',self.y_train.shape) #debug

  def init_model(self):
    model = Sequential()
    model.add(Dense(10, input_dim=8))
    model.add(Activation('relu'))
    model.add(Dense(10, input_dim=8))
    model.add(Activation('relu'))
    model.add(Dense(10, input_dim=8))
    model.add(Activation('relu'))
    
    model.add(Dense(2))
    model.add(Activation('softmax'))

    model.compile(optimizer='rmsprop', loss='kullback_leibler_divergence', metrics=['accuracy'])
    self.model = model
    return model
  
  def run_network(self, epochs=20, batch=1):
    try:
      if self.model is None:
            self.model = init_model()
      history = LossHistory()
      history = self.model.fit( 
                                self.X_train, self.y_train,
                                epochs=epochs,batch_size=batch,
                                callbacks=[history],
                                verbose=1
                               )
      loss, acc =self.model.evaluate(self.X_train, self.y_train) #加這行評估模型
      print(acc)
      return history.history

    except KeyboardInterrupt:
        print (' KeyboardInterrupt')
        return model, history.losses

import numpy as np
from matplotlib import pyplot as plt

pima = np.loadtxt('./pima-indians-diabetes.data',delimiter=',')

# Various preprocessing steps
pima[np.where(pima[:,0]>8),0] = 8

pima[np.where(pima[:,7]<=30),7] = 1
pima[np.where((pima[:,7]>30) & (pima[:,7]<=40)),7] = 2
pima[np.where((pima[:,7]>40) & (pima[:,7]<=50)),7] = 3
pima[np.where((pima[:,7]>50) & (pima[:,7]<=60)),7] = 4
pima[np.where(pima[:,7]>60),7] = 5

pima[:,:8] = pima[:,:8]-pima[:,:8].mean(axis=0)
pima[:,:8] = pima[:,:8]/pima[:,:8].var(axis=0)

trainin = pima[::2,:8]
testin = pima[1::2,:8]
traintgt = pima[::2,8:9]
testtgt = pima[1::2,8:9]
traintgt = to_categorical(traintgt)
testtgt = to_categorical(testtgt)
print(trainin.shape)
print(testin.shape)
print(traintgt.shape)
print(testtgt.shape)

pima_solution = Solution(trainin,traintgt,testin,testtgt)

pima_solution.init_model()
import time
start_time = time.time()
history = pima_solution.run_network(epochs=20, batch=1)
print("--- %s seconds ---" % (time.time() - start_time))
#print(losses)
plot_losses(history)