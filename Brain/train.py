import os
os.environ["TF_USE_LEGACY_KERAS"] ="1"

from intent.train import RawData, JointIntentAndSlotFillingModel, read_train_json_file
from intent.train.slot import encode_slots
import tensorflow as tf
from transformers import AutoTokenizer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from intent.train.encode import encode_intents, encode_texts

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

joint_model = JointIntentAndSlotFillingModel(model_name,
    intent_num_labels=len(intent_map), slot_num_labels=len(slot_map))

opt = Adam(learning_rate=3e-5, epsilon=1e-08)
losses = [SparseCategoricalCrossentropy(from_logits=True),
          SparseCategoricalCrossentropy(from_logits=True)]
metrics = [SparseCategoricalAccuracy("accuracy")]
# compile model
joint_model.compile(optimizer=opt, loss=losses, metrics=metrics)

x = {"input_ids": encoded_texts["input_ids"], "token_type_ids": encoded_texts["token_type_ids"],  "attention_mask": encoded_texts["attention_mask"]}

history = joint_model.fit(
    x, (encoded_slots, encoded_intents), epochs=1, batch_size=32, shuffle=True)

if not os.path.exists("./intent/models"):
    os.mkdir("./intent/models")

joint_model.save("./intent/models/model1")

def nlu(text, tokenizer, model, intent_names, slot_names):
    inputs = tf.constant(tokenizer.encode(text))[None, :]  # batch_size = 1
    outputs = model(inputs)
    slot_logits, intent_logits = outputs

    slot_ids = slot_logits.numpy().argmax(axis=-1)[0, :]
    intent_id = intent_logits.numpy().argmax(axis=-1)[0]

    info = {"intent": intent_names[intent_id], "slots": {}}

    out_dict = {}
    # get all slot names and add to out_dict as keys
    predicted_slots = set([slot_names[s] for s in slot_ids if s != 0])
    for ps in predicted_slots:
      out_dict[ps] = []

    # check if the text starts with a small letter
    if text[0].islower():
      tokens = tokenizer.tokenize(text, add_special_tokens=True)
    else:
      tokens = tokenizer.tokenize(text)
    for token, slot_id in zip(tokens, slot_ids):
        # add all to out_dict
        slot_name = slot_names[slot_id]

        if slot_name == "<PAD>":
            continue

        # collect tokens
        collected_tokens = [token]
        idx = tokens.index(token)

        # see if it starts with ##
        # then it belongs to the previous token
        if token.startswith("##"):
          # check if the token already exists or not
          if tokens[idx - 1] not in out_dict[slot_name]:
            collected_tokens.insert(0, tokens[idx - 1])

        # add collected tokens to slots
        out_dict[slot_name].extend(collected_tokens)

    # process out_dict
    for slot_name in out_dict:
        tokens = out_dict[slot_name]
        slot_value = tokenizer.convert_tokens_to_string(tokens)

        info["slots"][slot_name] = slot_value.strip()

    return info

print(nlu("add Madchild to Electro Latino", tokenizer, joint_model, 
    intent_names, slot_names))