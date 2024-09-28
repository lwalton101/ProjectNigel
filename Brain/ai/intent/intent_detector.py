import os
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
class IntentDetector:
    def __init__(self, model_name: str) -> None:
        self.load_model(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
    def load_model(self, model_name: str) -> None:
        self.model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
        pass
        
    def detect_intent(self, text_input: str):
        inputs = self.tokenizer(text_input, return_tensors="tf")
        outputs = self.model(**inputs).logits
        predicted_class_id = int(tf.math.argmax(outputs, axis=-1)[0])
        return self.model.config.id2label[predicted_class_id]