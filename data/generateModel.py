from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
import numpy as np
import tensorflow as tf
import pathlib
appDir = str(pathlib.Path().resolve())
print(appDir)


def geraModelo():
    classifier = Sequential()
    # Passo 1 - Primeira Camada de Convolução
    classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

    # Passo 2 - Pooling | Reduz a amostra da entrada ao longo de suas dimensões espaciais , obtendo o valor máximo em uma janela de entrada.
    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Adicionando a Segunda Camada de Convolução
    classifier.add(Conv2D(32, (3, 3), activation = 'relu'))

    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Passo 3 - Flattening -> Nivela a entrada. Não afeta o tamanho do lote / Achata a camada
    classifier.add(Flatten())

    # Passo 4 - Conexão entre camadas
    classifier.add(Dense(units = 128, activation = 'relu'))
    classifier.add(Dense(units = 1, activation = 'sigmoid')) # predição de 2 elementos

    # Compilando a rede
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy']) 
    
    # Criando os objetos train_datagen e validation_datagen com as regras de pré-processamento das imagens
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

    validation_datagen = ImageDataGenerator(rescale = 1./255)

    # Pré-processamento das imagens de treino e validação
    training_set = train_datagen.flow_from_directory(appDir+'/data/data_set_fish/train',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

    validation_set = validation_datagen.flow_from_directory(appDir+'/data/data_set_fish/validation',
                                                        target_size = (64, 64),
                                                        batch_size = 32,
                                                        class_mode = 'binary')

    # Executando o treinamento 
    history = classifier.fit(training_set,
                         steps_per_epoch = len(training_set),
                         epochs = 20,
                         validation_steps = len(validation_set))

    classifier.save(appDir+'/data/model.h5')
    
  

geraModelo()