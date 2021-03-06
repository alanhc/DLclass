# -*- coding: utf-8 -*-
"""week12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vkc5xonf-teP-I0BXE93Aj7gjIXvG2_F
"""



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

np.random.seed(25)

# Load MNIST dataset is provided by Keras.
(train_data, train_label), (test_data, test_label) = mnist.load_data()

print(" train_data original shape", train_data.shape)
print(" train_label original shape", train_label.shape)
print(" test_data original shape", test_data.shape)
print(" test_label original shape", test_label.shape)

#Show example image and its label
plt.imshow(train_data[0], cmap='gray')
plt.title('Class '+ str(train_label[0]))

#Reshape the data and normalize the data
train_data = train_data.reshape(train_data.shape[0], 28, 28, 1)
test_data = test_data.reshape(test_data.shape[0], 28, 28, 1)

train_data = train_data.astype('float32')
test_data = test_data.astype('float32')

train_data /=255
test_data /=255


# Test the shape
print(train_data.shape)

# one-hot encode the labels
number_of_classes = 10

train_onehot_label = np_utils.to_categorical(train_label, number_of_classes)
test_onehot_label = np_utils.to_categorical(test_label, number_of_classes)

# test the sample result
train_label[0], train_onehot_label[0]


# Three steps to create a CNN
# 1. Convolution
# 2. Activation
# 3. Pooling
# Repeat Steps 1,2,3 for adding more hidden layers

# 4. After that make a fully connected network
# This fully connected network gives ability to the CNN
# to classify the samples

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(28,28,1)))
model.add(BatchNormalization(axis=-1))
convout1 = Activation('relu')
model.add(convout1)
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
convout2 = MaxPooling2D(pool_size=(2,2))
model.add(convout2)

model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization(axis=-1))
convout3 = Activation('relu')
model.add(convout3)
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
convout4 = MaxPooling2D(pool_size=(2,2))
model.add(convout4)

model.add(Flatten())

# Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))

model.add(Activation('softmax'))

#print the model
model.summary()

#compile the model
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Use Data Augmentation
gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3, height_shift_range=0.08, zoom_range=0.08)
test_gen = ImageDataGenerator()

train_generator = gen.flow(train_data, train_onehot_label, batch_size=64)
test_generator = test_gen.flow(test_data, test_onehot_label, batch_size=64)

# model.fit(train_data, train_onehot_label, batch_size=128, nb_epoch=1, validation_data=(test_data, test_onehot_label))

model.fit_generator(train_generator, steps_per_epoch=60000//64, epochs=5, 
                    validation_data=test_generator, validation_steps=10000//64)

print(train_data[0].shape)

img_to_visualize = train_data[0]
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