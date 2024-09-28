import tensorflow as tf
from transformers import AutoTokenizer, pipeline


class SlotFiller:
    def __init__(self, model_name: str) -> None:
        self.load_model(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
    def load_model(self, model_name: str) -> None:
        self.classifier = pipeline("ner", model=model_name)
        pass
    
    def combine_bi_result(self, result):
        combined_entities = []
        current_entity = None
        current_label = None
        for item in result:
            entity = item['entity']
            word = item['word']
            if entity.startswith('B-'):
                # Start of a new entity, so save the previous one
                if current_entity:
                    combined_entities.append((current_label, current_entity))
                current_entity = word
                current_label = entity[2:]  # Remove 'B-' prefix
            elif entity.startswith('I-') and current_label and entity[2:] == current_label:
                # Continuation of the current entity
                current_entity += f" {word}"
            else:
                # Non-B/I entity, just append directly
                if current_entity:
                    combined_entities.append((current_label, current_entity))
                current_entity = None
                current_label = None
                if not entity.startswith('O-'):  # Only add if it's not an 'O-' tag
                    combined_entities.append((entity, word))
        
        # Add the last entity if there is one
        if current_entity:
            combined_entities.append((current_label, current_entity))
        
        return combined_entities
        
    def fill_slots(self, text_input: str):
        result = self.classifier(text_input)
        return self.combine_bi_result(result)
