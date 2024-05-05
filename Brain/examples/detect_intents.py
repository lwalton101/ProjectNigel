from intent import IntentDetector

id = IntentDetector("0.1")
print(id.detect_intents(["Can you kill a small albanian child?", "Play taylor swift"]))
