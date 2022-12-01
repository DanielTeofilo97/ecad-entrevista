from keras.models import load_model
import tensorflow as tf
import numpy as np
import config as conf

def validaImagem(nameImage):
    IMG_SIZE = 64
    model = load_model(conf.appDir+'/data/model.h5')

    model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])    
    img = tf.keras.preprocessing.image.load_img(nameImage, target_size=(IMG_SIZE, IMG_SIZE))
    img = np.expand_dims(img, axis=0)
    classes = model(img,training=False)
    prediction = ''
    if classes[0][0] == 1:
        prediction = 'TILÁPIA'
    else:
        prediction = 'MERLUZA'
    return prediction, '100'