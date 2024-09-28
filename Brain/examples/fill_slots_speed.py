from ..ai.intent import IntentDetector
import datetime
from ..ai.slot import SlotFiller

id = SlotFiller("Nicknotname/Project_Nigel_Intent_Detection")
startTime = datetime.datetime.now()

tries = 100
print("Starting Test")
for x in range(tries):
    id.fill_slots("Play hello by adele")
    
print(f"Total Tries: {tries}")
print(f"Total Time: {datetime.datetime.now() - startTime}")
print(f"Avg Time per Try: {(datetime.datetime.now() - startTime)/tries}")