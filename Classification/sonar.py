import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_data(path, batch_size=32, ratio_train_test=0.7):
    data = pd.read_csv(path)
    inputs = data[data.columns[:60]].values
    labels = data[data.columns[60]].values
    dataset_size = len(labels)
    total_batch = int(dataset_size*ratio_train_test / batch_size)
    encoder = LabelEncoder()
    labels = encoder.fit_transform(labels) # Assign a unique integer for each label
    dataset = tf.data.Dataset.from_tensor_slices((inputs, labels)).shuffle(buffer_size=dataset_size)
    dataset = dataset.map(lambda input, labels: (tf.cast(input, tf.float32), tf.one_hot(labels, 2)))
    train_dataset = dataset.take(int(ratio_train_test * dataset_size)).repeat().batch(batch_size=batch_size)
    test_dataset = dataset.skip(int(ratio_train_test * dataset_size)).repeat().batch(batch_size=batch_size)
    print("Size dataset: {}, size train dataeset: {}, size test dataset: {}".format(dataset_size, int(ratio_train_test*dataset_size), dataset_size - int(ratio_train_test*dataset_size)))
    return train_dataset, test_dataset, total_batch



def get_loss (logits, labels):
    return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=batch_y))



if __name__ == '__main__':
    train_dataset, test_dataset, number_batches = load_data("data/sonar.csv", batch_size=1)
    dataset_train_iter = iter(train_dataset)
    dataset_test_iter = iter(test_dataset)
    optimizer = tf.keras.optimizers.Adam()


    model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=128, activation=tf.keras.activations.relu, input_shape=(60, )),
            tf.keras.layers.Dense(units=2, activation=tf.keras.activations.softmax)
    ])

    model.compile(loss='categorical_crossentropy',
          optimizer='adam',
          metrics=['accuracy'])

    history = model.fit(train_dataset, epochs=80, steps_per_epoch=number_batches, validation_data=test_dataset, validation_steps=number_batches)


    #print(history.history)

    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()
