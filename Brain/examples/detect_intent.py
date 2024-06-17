from Brain.intent import IntentDetector

id = IntentDetector("0.1")
print(id.detect_intent("Can you kill a small albanian child?"))
