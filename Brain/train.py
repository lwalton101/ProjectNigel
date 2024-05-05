# %%
import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow import keras
from keras import layers,losses
batch_size = 32
seed = 42

modelName = input("Enter model name: ")
raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    'intent/train/dataset/',
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

i = 0
for label_name in raw_train_ds.class_names:
    print(f"Label {i} is {label_name}")
    i += 1

raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    'intent/train/dataset/',
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)

def custom_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
  return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation),
                                  '')

max_features = 10000
sequence_length = 250

vectorize_layer = layers.TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

text_batch, label_batch = next(iter(raw_train_ds))
first_review, first_label = text_batch[0], label_batch[0]
print("Review", first_review)
print("Label", raw_train_ds.class_names[first_label])
print("Vectorized review", vectorize_text(first_review, first_label))

print("1287 ---> ",vectorize_layer.get_vocabulary()[1287])
print(" 313 ---> ",vectorize_layer.get_vocabulary()[313])
print('Vocabulary size: {}'.format(len(vectorize_layer.get_vocabulary())))

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

embedding_dim = 16
model = tf.keras.Sequential([
  layers.Embedding(max_features, embedding_dim),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(7, activation='sigmoid')])

model.summary()

model.compile(loss=losses.SparseCategoricalCrossentropy(),
              optimizer='adam',
              metrics=['accuracy'])

epochs = 10
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

export_model = tf.keras.Sequential([
  vectorize_layer,
  model,
  layers.Activation('sigmoid')
])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)

examples = tf.constant([
  "Play Bad Blood by Taylor Swift",
  "Get the weather in Southern Ohio",
  "Can you add a song to my bops playlist"
])

predictions = export_model.predict(examples)
j = [raw_train_ds.class_names[prediction.argmax()] for prediction in predictions]
if not os.path.exists("./intent/train/models"):
  os.mkdir("./intent/train/models")
modelLoc = f"./intent/train/models/{modelName}"
export_model.export(modelLoc)

with open(f"{modelLoc}/intents.txt", "w") as f:
  f.write("\n".join(raw_train_ds.class_names))


