import tensorflow as tf
from tensorflow import keras

import numpy as np

def init_nn(size):

  print("\n\n##### Creating neural net #####\n")

  # Create the network
  model = keras.Sequential([
    keras.layers.Dense(size**2, input_shape=((size**2)-1, )),
    keras.layers.Dense((size**2) / 2, activation='relu'),
    keras.layers.Dense(1)
  ])

  # Compile the model
  model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
  )

  input_layer = model.layers[0]
  print("Created neural net with input size", input_layer.input_shape)

  return model


if (__name__=="__main__"):
  model = init_nn(4)
  test_state = np.asarray([(1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])
  prediction = model.predict(test_state)[0][0] # predict returns a 2D array, so we get the prediction value by using [0][0]
  print(prediction)