
import timeit


setupStatement = "from intent import IntentDetector\nid = IntentDetector(\"0.1\")"
executeStatement = "id.detect_intent(\"What is the weather like in Auckland, New Zealand right now\")"

timer = timeit.timeit(executeStatement, setupStatement, number=10000)
print(timer/10000)