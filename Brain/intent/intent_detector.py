import tensorflow as tf
from keras import layers

class IntentDetector:
    def __init__(self, model_name: str) -> None:
        self.load_model(model_name)
        
    def load_model(self, model_name: str) -> None:
        self.model_name = model_name
        self.model_path = f"./intent/train/models/{model_name}"
        self.layer = layers.TFSMLayer(self.model_path)
        self.intents = []
        with open(f"{self.model_path}/intents.txt") as f:
            self.intents = [x.strip() for x in f.readlines()]
        
    def detect_intent(self, text_input: str) -> str:
        input_tensor = tf.constant([text_input], dtype=tf.string)
        input_tensor = tf.reshape(input_tensor, shape=(1,)) 
        evaluation = self.layer(input_tensor)
        return self.intents[tf.argmax(evaluation, axis=1).numpy()[0]]
    
    def detect_intents(self, text_inputs: str) -> str:
        input_tensor = tf.constant(text_inputs, dtype=tf.string)
        input_tensor = tf.reshape(input_tensor, shape=(len(text_inputs),)) 
        evaluation = self.layer(input_tensor)
        results = []
        for x in range(len(text_inputs)):
            resultArr = evaluation[x]
            highestIndex = tf.argmax(resultArr, axis=0)
            results.append(self.intents[highestIndex])

        return results
        
        