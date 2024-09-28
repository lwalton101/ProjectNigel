from ..ai.slot import SlotFiller
from ..ai.intent import IntentDetector

intent_detector = IntentDetector("Nicknotname/Project_Nigel_Intent_Detection")
slot_filler = SlotFiller("Nicknotname/Project_Nigel_Slot_Filling")
prompt = "Play hello by adele"

intent = intent_detector.detect_intent(prompt)
slots = slot_filler.fill_slots(prompt)

print(f"Intent: {intent}")
if intent != "greeting":
    for slot in slots:
        print(f"{slot[0]}: {slot[1]}")
else:
    print("No slots needed")