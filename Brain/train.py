from intent.train import RawData, read_train_json_file
import tensorflow as tf
from transformers import AutoTokenizer

def encode_texts(tokenizer, texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="tf")

def encode_intents(intents, intent_map):
    encoded = []
    for i in intents:
        encoded.append(intent_map[i])
    # convert to tf tensor
    return tf.convert_to_tensor(encoded, dtype="int32")

train_data: list[RawData] = read_train_json_file("./intent/train/train.json")

model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

texts = [d.text for d in train_data]
tds = encode_texts(tokenizer, texts)
encoded_texts = tds

intents = [d.intent for d in train_data]
intent_names = list(set(intents))

intent_map = dict() # index -> intent
for idx, ui in enumerate(intent_names):
    intent_map[ui] = idx

encoded_intents = encode_intents(intents, intent_map)