from ..ai.slot import SlotFiller

id = SlotFiller("Nicknotname/Project_Nigel_Slot_Filling")
slots = id.fill_slots("yo wagwan i want you to Play hello from the other side which was made by Big steve and the red bananas")

for slot in slots:
    print(f"{slot[0]}: {slot[1]}")
