from ..ai.intent import IntentDetector

id = IntentDetector("0.1")
print(id.detect_intent("Play hello by adele"))
