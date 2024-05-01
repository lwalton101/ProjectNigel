import json
import os

class RawData(object):
    def __init__(self, id, intent, positions, slots, text):
        self.id = id
        self.intent = intent
        self.positions = positions
        self.slots = slots
        self.text = text

    def __repr__(self):
        return str(json.dumps(self.__dict__, indent=2))
    
def read_train_json_file(filename):
    if os.path.exists(filename):
        intents = []

        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

            for k in data.keys():
                intent = data[k]["intent"]
                positions = data[k]["positions"]
                slots = data[k]["slots"]
                text = data[k]["text"]

                temp = RawData(k, intent, positions, slots, text)
                intents.append(temp)

        return intents
    else:
        raise FileNotFoundError("No file found with that path!")

