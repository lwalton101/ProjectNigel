import os
import re
import json
import random

NUM_TO_GEN = 10000

vars = {}
templates = {}

# Load vars from the files
for file in os.listdir("./vars"):
    with open(f"./vars/{file}") as f:
        lines = [x.strip() for x in f.readlines()]
        vars[file.replace(".txt", "")] = lines

# Load templates from the files
for file in os.listdir("./templates"):
    with open(f"./templates/{file}") as f:
        lines = [x.strip() for x in f.readlines()]
        templates[file.replace(".txt", "")] = lines

ner_mapping = {
    "SongName": (1, 2),  # (B-SongName, I-SongName)
    "ArtistName": (3, 4),  # (B-ArtistName, I-ArtistName)
#    "PreRequest": (5, 6),  # (B-PreRequest, I-PreRequest)
}

def generate_random_permutations(template, vars, ner_mapping, num_to_generate):
    template_parts = re.split(r'(\$[a-zA-Z0-9_]+)', template)
    placeholders = [part[1:] for part in template_parts if part.startswith('$')]
    
    values = []
    for placeholder in placeholders:
        if placeholder in vars:
            values.append(vars[placeholder])
        else:
            raise KeyError(f"Variable '{placeholder}' not found in vars.")
    
    result_sentences = []
    attempts = 0
    max_attempts = num_to_generate * 10  # Safeguard against infinite loops
    
    while len(result_sentences) < num_to_generate and attempts < max_attempts:
        sentence_parts = []
        ner_tags = []
        
        for part in template_parts:
            if part.startswith('$'):
                value_list = vars[part[1:]]
                
                if not value_list:  # Check if the list is empty
                    #print(f"Warning: No values found for placeholder '{part}'")
                    continue  # Skip to the next part of the template
                
                value = random.choice(value_list)
                value_tokens = value.split()
                
                if not value_tokens:  # Check if the token list is empty
                    #print(f"Warning: Selected value is empty for placeholder '{part}'")
                    continue  # Skip if there's no token
                
                # Assign integer NER tags for B and I
                tag_ids = ner_mapping.get(part[1:], (0, 0))  # Default to (0, 0) if not found
                
                # Assign the B-tag for the first token
                sentence_parts.append(value_tokens[0])  # First token
                ner_tags.append(tag_ids[0])  # First token gets B-tag value
                
                # Assign I-tag for subsequent tokens
                for token in value_tokens[1:]:
                    sentence_parts.append(token)  # Remaining tokens
                    ner_tags.append(tag_ids[1])  # Subsequent tokens get I-tag value
            else:
                fixed_tokens = part.split()
                sentence_parts.extend(fixed_tokens)
                ner_tags.extend([0] * len(fixed_tokens))  # O-tag for fixed tokens, using 0 for "Outside"
        
        sentence = " ".join(sentence_parts)
        
        # Check if this exact sentence has already been generated
        if not any(s['tokens'] == sentence_parts for s in result_sentences):
            json_data = {
                'tokens': sentence_parts,
                'ner_tags': ner_tags
            }
            result_sentences.append(json_data)
        
        attempts += 1
    
    return result_sentences


output_dir = './data'
os.makedirs(output_dir, exist_ok=True)

id_counter = 0
for template_name, template_list in templates.items():
    all_sentences = []
    for template in template_list:
        try:
            sentences = generate_random_permutations(template, vars, ner_mapping, NUM_TO_GEN)
            for sentence_data in sentences:
                sentence_data['id'] = str(id_counter)
                all_sentences.append(sentence_data)
                id_counter += 1
        except KeyError as e:
            print(f"Error in template '{template}': {e}")
    
    output_filename = os.path.join(output_dir, f"{template_name}.json")
    with open(output_filename, 'w') as json_file:
        json.dump(all_sentences, json_file, indent=4)

print(f"All templates processed. Generated up to {NUM_TO_GEN} random permutations per template and saved as JSON files.")
