import os

vars = {}
for file in os.listdir("./vars"):
    f = open(f"./vars/{file}")
    lines = [x.strip() for x in f.readlines()]
    vars[file.replace(".txt", "")] = lines
    
print(vars)