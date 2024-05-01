import tensorflow as tf


def encode_texts(tokenizer, texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="tf")

def encode_intents(intents, intent_map):
    encoded = []
    for i in intents:
        encoded.append(intent_map[i])
    # convert to tf tensor
    return tf.convert_to_tensor(encoded, dtype="int32")