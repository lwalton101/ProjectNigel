import numpy as np

def get_slot_from_word(word, slot_dict):
    for slot_label,value in slot_dict.items():
        if word in value.split():
            return slot_label
    return None

def encode_slots(all_slots, all_texts,
                 tokenizer, slot_map, max_len):
    encoded_slots = np.zeros(shape=(len(all_texts), max_len), dtype=np.int32)

    for idx, text in enumerate(all_texts):
        enc = [] # for this idx, to be added at the end to encoded_slots

        # slot names for this idx
        slot_names = all_slots[idx]

        # raw word tokens
        # not using bert for this block because bert uses
        # a wordpiece tokenizer which will make
        # the slot label to word mapping
        # difficult
        raw_tokens = text.split()

        # words or slot_values associated with a certain
        # slot_name are contained in the values of the
        # dict slots_names
        # now this becomes a two way lookup
        # first we check if a word belongs to any
        # slot label or not and then we add the value from
        # slot map to encoded for that word
        for rt in raw_tokens:
            # use bert tokenizer
            # to get wordpiece tokens
            bert_tokens = tokenizer.tokenize(rt)

            # find the slot name for a token
            rt_slot_name = get_slot_from_word(rt, slot_names)
            if rt_slot_name is not None:
                # fill with the slot_map value for all ber tokens for rt
                enc.append(slot_map[rt_slot_name])
                enc.extend([slot_map[rt_slot_name]] * (len(bert_tokens) - 1))

            else:
                # rt is not associated with any slot name
                enc.append(0)


        # now add to encoded_slots
        # ignore the first and the last elements
        # in encoded text as they're special chars
        encoded_slots[idx, 1:len(enc)+1] = enc

    return encoded_slots
