import os
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
class IntentDetector:
    def __init__(self, model_name: str) -> None:
        self.load_model(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
    def load_model(self, model_name: str) -> None:
        self.model = TFAutoModelForSequenceClassification.from_pretrained(f"./Brain/ai/intent/models/{model_name}")
        pass
        
    def detect_intent(self, text_input: str):
        inputs = self.tokenizer(text_input, return_tensors="tf")
        outputs = self.model(**inputs).logits
        return outputs