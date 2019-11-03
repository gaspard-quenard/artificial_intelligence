import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os


def create_model():
    model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="SAME", activation=tf.keras.activations.relu, input_shape=(24,24, 3), kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=(2, 2), padding="SAME", activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="SAME", activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=(2, 2), padding="SAME", activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.Dense(128, activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.Dense(64, activation=tf.keras.activations.relu, kernel_regularizer=tf.keras.regularizers.l2(l=0.001)),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Softmax()
        ])
    return model


def create_dataset(x, y, batch_size=256):
    # loat the data

    #(y_train.shape)
    x = tf.cast(x, dtype=tf.float32) / 255.

    #print("X train shape: {}".format(x_train.shape))
    # Create the training, and testing dataset
    dataset = tf.data.Dataset.from_tensor_slices((x, y)).repeat().shuffle(buffer_size=len(y)).batch(batch_size=batch_size)
    dataset = dataset.map(lambda a, b: (tf.image.central_crop(a, 0.7), b))
    #print(train_dataset)

    return dataset




if __name__ == '__main__':
    batch_size = 256
    model_path = "./results/cifer10.h5"

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    train_dataset = create_dataset(x_train, y_train)
    test_dataset  = create_dataset(x_test, y_test)
    dataset_train_iter = iter(train_dataset)
    dataset_test_iter = iter(test_dataset)


    model = create_model()

    #compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                 loss=tf.keras.losses.sparse_categorical_crossentropy,
                 metrics=["accuracy"])



    # train the network
    history = model.fit(train_dataset, epochs=10, steps_per_epoch=50000//batch_size,
                        validation_data=test_dataset, validation_steps=3)
    #save the model

    model.save(model_path)
    print("Model saved at: {}".format(model_path))

    #model = tf.keras.models.load_model(model_path)
