import json
import os


data = []
with open("./intent/train/snips.json") as f:
    data = json.load(f)
    
di = {}
for x in data:
    text = x[0]
    intent = x[1]
    if not os.path.exists(f"./intent/train/dataset/{intent}"):
        os.mkdir(f"./intent/train/dataset/{intent}")
    
    if intent not in di.keys():
        di[intent] = 0
        
    f = open(f"./intent/train/dataset/{intent}/{di[intent]}.txt", "w", encoding="utf-8")    
    f.write(text)
    f.close()
    di[intent] += 1   