from intent.train import RawData, read_train_json_file
from intent.train.slot import encode_slots
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

slot_names = set()
for td in train_data:
    slots = td.slots
    for slot in slots:
        slot_names.add(slot)
slot_names = list(slot_names)
slot_names.insert(0, "<PAD>")

slot_map = dict() # slot -> index
for idx, us in enumerate(slot_names):
    slot_map[us] = idx

max_len = len(encoded_texts["input_ids"][0])
all_slots = [td.slots for td in train_data]
all_texts = [td.text for td in train_data]
encoded_slots = encode_slots(all_slots, all_texts, tokenizer, slot_map, max_len)