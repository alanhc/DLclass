# -*- coding: utf-8 -*-
"""week11.ipynb 的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/135sZMiufTr-NEV0wHb4IGH_VVC5YTGvo
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
import tensorflow
print(tensorflow.__version__)
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('drive/My Drive/dataset/intel_small')

!ls

train_path = 'seg_train'
test_path = 'seg_test'
cat = os.listdir(train_path)
print(f'We have {len(cat)} classes: ', os.listdir(train_path))
# Examples of images
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
rows, cols = (1, 5)

for c in cat:
    print(f'{c} images:')
    path = f'{train_path}/{c}'    
    fig = plt.figure(figsize = (13, 8))
    for i in range(rows * cols):
        fig.add_subplot(rows, cols, i+1)
        image_id = os.listdir(path)[np.random.randint(0, 100)]
        image = cv.imread(path + f'/{image_id}')
        plt.imshow(image[:, :, ::-1])
        plt.title(image_id)
        plt.axis('off')
    plt.show()

from keras.preprocessing.image import ImageDataGenerator
# Parameters of model
target_size = (150,150)
colormode = 'rgb'
seed = 666
batch_size = 1
input_shape = (150, 150)
reg = None # l2(0.0001)
axis = -1 # For BatchNormalization layers

# Creating ImageDataGenerator, which rescales images 
# and splits train data into train and validation sets 
# with 0.9 / 0.1 proportion
datagen = ImageDataGenerator(rescale = 1.0/255.0,
                            validation_split = 0.1
                            )

# Creating train, valid and test generators
train_generator = datagen.flow_from_directory(directory = train_path, # Path to directory which contains images classes
                                             target_size = target_size, # Whether resize images or not
                                             color_mode = colormode, 
                                             #batch_size = batch_size,
                                             class_mode = 'categorical',
                                             #shuffle = True,
                                             #seed = seed,
                                             subset = 'training') # Train or validation dataset

valid_generator = datagen.flow_from_directory(directory = train_path,
                                             target_size = target_size,
                                             color_mode = colormode,
                                             #batch_size = batch_size,
                                             class_mode = 'categorical',
                                             #shuffle = True,
                                             #seed = seed,
                                             subset = 'validation')

test_generator = datagen.flow_from_directory(directory = test_path,
                                            target_size = target_size,
                                            color_mode = colormode,
                                            batch_size = 1,
                                            class_mode = None,
                                            shuffle = False, 
                                            seed = seed)

# Define number of steps for fit_generator function
STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = valid_generator.n // valid_generator.batch_size

train_generator.

from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout,BatchNormalization,Conv2D,MaxPooling2D
from keras.optimizers import RMSprop, SGD, Adam
import time
from keras.callbacks import ModelCheckpoint
def plot_losses(history_labels):
  for history, label in history_labels:
    plt.figure(1, figsize=(10,10)) 
    plt.subplot(211)   # 2 by 1 array of subplots, and draw the first one 
    plt.plot(history['loss'])  
    plt.plot(history['val_loss'])  
    plt.title('model loss ' + label)  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'validation'], loc='upper right')  
	
    plt.subplot(212)   # 2 by 1 array of subplots, and draw the second one 
    plt.plot(history['accuracy'])  
    plt.plot(history['val_accuracy'])  
    plt.title('model accuracy ' + label)  
    plt.ylabel('acc')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'validation'], loc='lower right')  	
    plt.show()

from keras import regularizers
# Defining model architecture
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(150,150,3)))
model.add(BatchNormalization(axis=-1))
convout1=Activation('relu')
model.add(convout1)
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
convout2=MaxPooling2D(pool_size=(2,2))
model.add(convout2)

model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization(axis=-1))
convout3=Activation('relu')
model.add(convout3)
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
convout4=MaxPooling2D(pool_size=(2,2))
model.add(convout4)

model.add(Flatten())

# Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.4))
model.add(Dense(6))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
model.summary()

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
#checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = model.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 30, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')

print(train_generator[0][0].shape)

img_to_visualize = train_generator[0][0][50]
img_to_visualize.shape

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#for IPython, can not be used in PYTHON IDE
# %matplotlib inline  
import matplotlib # 注意也要import一次
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D
from keras.layers.advanced_activations import LeakyReLU 
from keras.preprocessing.image import ImageDataGenerator

from keras import backend as K
img_to_visualize = train_generator[0][0][0]
img_to_visualize = np.expand_dims(img_to_visualize, axis=0)

def layer_to_visualize(layer):
    inputs = [K.learning_phase()] + model.inputs #[ boolean:是否訓練, 網路的輸入層(圖片)]

    _convout1_f = K.function(inputs, [layer.output]) #從輸入到圖層的輸出
    def convout1_f(X):
        # The [0] is to disable the training phase flag
        return _convout1_f([0] + [X]) #一定設為非訓練階段

    convolutions = convout1_f(img_to_visualize)
    print(np.asarray(convolutions).shape) #(1, 1, x, y, channel)
    convolutions = np.rollaxis(np.asarray(convolutions), 4, 1) #change order from channel-last to channel-first
    convolutions = np.squeeze(convolutions) #remove single-dimensional entries

    print ('Shape of conv:', convolutions.shape)
    print('len of conv:', len(convolutions))
    n = convolutions.shape[0]
    n = int(np.ceil(np.sqrt(n)))
    
    # Visualization of each filter of the layer
    fig = plt.figure(figsize=(12,8))#width and height of each figure
    for i in range(len(convolutions)):
        ax = fig.add_subplot(n,n,i+1) #plot at (i+1) of n * n figures
        ax.imshow(convolutions[i], cmap='gray')
    


# Specify the layer to want to visualize
layer_to_visualize(convout1) #shape: (26, 26, 32)

# As convout2 is the result of a MaxPool2D layer
# We can see that the image has blurred since
# the resolution has reduced 
layer_to_visualize(convout2)
layer_to_visualize(convout3)
layer_to_visualize(convout4)

from keras import regularizers
# Defining model architecture
model2 = Sequential()

model2.add(Conv2D(128, (3, 3), input_shape=(150,150,3)))
model2.add(BatchNormalization(axis=-1))
model2.add(Activation('relu'))
model2.add(Conv2D(128, (3, 3)))
model2.add(BatchNormalization(axis=-1))
model2.add(Activation('relu'))
model2.add(MaxPooling2D(pool_size=(2,2)))

model2.add(Conv2D(256,(3, 3)))
model2.add(BatchNormalization(axis=-1))
model2.add(Activation('relu'))
model2.add(Conv2D(256, (3, 3)))
model2.add(BatchNormalization(axis=-1))
model2.add(Activation('relu'))
model2.add(MaxPooling2D(pool_size=(2,2)))


model2.add(Flatten())

# Fully connected layer
model2.add(Dense(512))
model2.add(BatchNormalization())
model2.add(Activation('relu'))
model2.add(Dropout(0.4))
model2.add(Dense(6))

model2.add(Activation('softmax'))

model2.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = model2.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(model2, show_shapes=True, show_layer_names=True, to_file='model.png')

from keras import regularizers
# Defining model architecture
model3 = Sequential()

model3.add(Conv2D(128, (3, 3), input_shape=(150,150,3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(Conv2D(128, (3, 3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(MaxPooling2D(pool_size=(2,2)))

model3.add(Conv2D(256,(3, 3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(Conv2D(256, (3, 3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(MaxPooling2D(pool_size=(2,2)))

model3.add(Conv2D(512,(3, 3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(Conv2D(512, (3, 3)))
model3.add(BatchNormalization(axis=-1))
model3.add(Activation('relu'))
model3.add(MaxPooling2D(pool_size=(2,2)))



model3.add(Flatten())

# Fully connected layer
model3.add(Dense(1024,kernel_regularizer=regularizers.l2(0.01)))
model3.add(BatchNormalization())
model3.add(Activation('relu'))
model3.add(Dense(1024,kernel_regularizer=regularizers.l2(0.01)))
model3.add(BatchNormalization())
model3.add(Activation('relu'))


model3.add(Dense(6))

model3.add(Activation('softmax'))

model3.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
model3.summary()

from keras.callbacks import EarlyStopping
# Defining checkpoint c                                                                                                                                                                                                                                                        -+allback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = model3.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(model3, show_shapes=True, show_layer_names=True, to_file='model.png')



"""## VGG16"""

from keras import regularizers
# Defining model architecture
vgg16 = Sequential()

vgg16.add(Conv2D(64, (3, 3), input_shape=(150,150,3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(64, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16.add(Conv2D(128, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(128, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16.add(Conv2D(256, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(256, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(256, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(Conv2D(512, (3, 3),padding="same"))
vgg16.add(Activation('relu'))

vgg16.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16.add(Flatten())

# Fully connected layer
vgg16.add(Dense(4096))
vgg16.add(Activation('relu'))
vgg16.add(Dense(4096))
vgg16.add(Activation('relu'))
vgg16.add(Dense(6))

vgg16.add(Activation('softmax'))

vgg16.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
vgg16.summary()

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = vgg16.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(vgg16, show_shapes=True, show_layer_names=True, to_file='model.png')

from keras import regularizers
# Defining model architecture
vgg16_new = Sequential()

vgg16_new.add(Conv2D(64, (3, 3), input_shape=(150,150,3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(64, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16_new.add(Conv2D(128, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(128, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16_new.add(Conv2D(256, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(256, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(256, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(Conv2D(512, (3, 3),padding="same"))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))

vgg16_new.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))

vgg16_new.add(Flatten())

# Fully connected layer
vgg16_new.add(Dense(4096))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))
vgg16_new.add(Dense(4096))
model.add(BatchNormalization(axis=-1))
vgg16_new.add(Activation('relu'))
vgg16_new.add(Dense(6))

vgg16_new.add(Activation('softmax'))

vgg16_new.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
vgg16_new.summary()

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = vgg16_new.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(vgg16_new, show_shapes=True, show_layer_names=True, to_file='model.png')

"""## Transfer learning"""

from keras.applications.vgg16 import VGG16
vgg16 = VGG16(include_top=False, input_shape=(150,150,3))
model = Sequential(vgg16.layers)
for layer in model.layers[:15]:
  layer.traninable = False
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.4))
model.add(Dense(6))
model.add(Activation('sigmoid'))
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
print(model.summary())

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = model.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')

"""## AlexNet
https://www.mydatahack.com/building-alexnet-with-keras/
"""

from keras import regularizers
# (3) Create a sequential model
model = Sequential()

# 1st Convolutional Layer
model.add(Conv2D(filters=96, input_shape=(224,224,3), kernel_size=(11,11),\
 strides=(4,4), padding='valid'))
model.add(Activation('relu'))
# Pooling 
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
# Batch Normalisation before passing it to the next layer
model.add(BatchNormalization())

# 2nd Convolutional Layer
model.add(Conv2D(filters=256, kernel_size=(11,11), strides=(1,1), padding='valid'))
model.add(Activation('relu'))
# Pooling
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
# Batch Normalisation
model.add(BatchNormalization())

# 3rd Convolutional Layer
model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())

# 4th Convolutional Layer
model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid'))
model.add(Activation('relu'))
# Batch Normalisation
model.add(BatchNormalization())

# 5th Convolutional Layer
model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='valid'))
model.add(Activation('relu'))
# Pooling
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
# Batch Normalisation
model.add(BatchNormalization())

# Passing it to a dense layer
model.add(Flatten())
# 1st Dense Layer
model.add(Dense(4096, input_shape=(150*150*3,)))
model.add(Activation('relu'))
# Add Dropout to prevent overfitting
model.add(Dropout(0.4))
# Batch Normalisation
model.add(BatchNormalization())

# 2nd Dense Layer
model.add(Dense(4096))
model.add(Activation('relu'))
# Add Dropout
model.add(Dropout(0.4))
# Batch Normalisation
model.add(BatchNormalization())

# 3rd Dense Layer
model.add(Dense(1000))
model.add(Activation('relu'))
# Add Dropout
model.add(Dropout(0.4))
# Batch Normalisation
model.add(BatchNormalization())

# Output Layer
model.add(Dense(6))
model.add(Activation('softmax'))


model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
model.summary()

from keras.callbacks import EarlyStopping
# Defining checkpoint callback
checkpoint = ModelCheckpoint('../model_save/call_back_history.hdf5', verbose = 1, monitor = 'val_accuracy', save_best_only = True)
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
# Fit model
import time
start_time = time.time()
history = model.fit_generator(generator = train_generator ,
                             steps_per_epoch = STEP_SIZE_TRAIN,
                             validation_data = valid_generator,
                             validation_steps = STEP_SIZE_VALID,
                             epochs = 200, callbacks = [es])
print ("Training duration : {0}".format(time.time() - start_time))  
history=history.history
from keras.utils import plot_model
labels = ['test']  
plot_losses(zip([history], labels) )	

plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')