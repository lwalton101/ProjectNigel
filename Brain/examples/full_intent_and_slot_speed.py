import datetime
from ..ai.slot import SlotFiller
from ..ai.intent import IntentDetector

intent_detector = IntentDetector("Nicknotname/Project_Nigel_Intent_Detection")
slot_filler = SlotFiller("Nicknotname/Project_Nigel_Slot_Filling")
prompt = "Play hello by adele"



startTime = datetime.datetime.now()

tries = 100
print("Starting Test")
for x in range(tries):
    intent = intent_detector.detect_intent(prompt)
    slots = slot_filler.fill_slots(prompt)
endTime = datetime.datetime.now()
print(f"Total Tries: {tries}")
print(f"Total Time: {endTime - startTime}")
print(f"Avg Time per Try: {(endTime - startTime)/tries}")