from ..ai.intent import IntentDetector
import datetime
id = IntentDetector("0.1")
startTime = datetime.datetime.now()

tries = 10000
print("Starting Test")
for x in range(tries):
    id.detect_intent("Play Hello by adele")
    
print(f"Total Tries: {tries}")
print(f"Total Time: {datetime.datetime.now() - startTime}")
print(f"Avg Time per Try: {(datetime.datetime.now() - startTime)/tries}")