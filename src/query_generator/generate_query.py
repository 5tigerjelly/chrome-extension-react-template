import spacy

nlp = spacy.load("en_core_web_sm")

def generate_clean_query(text):
    doc = nlp(text)

    # parts of speech to keep
    keep_pos = {"NOUN", "PROPN", "ADJ", "NUM"}
    keywords = [token.text for token in doc if token.pos_ in keep_pos]

    # extract named entities (i.e. dates, percentages, names)
    entities = [ent.text for ent in doc.ents]

    # merge POS and named entities and remove duplicates while preserving order
    all_terms = keywords + entities
    seen = set()
    deduped = []
    for word in all_terms:
        word = word.strip()
        if word and word.lower() not in seen:
            deduped.append(word)
            seen.add(word.lower())  # case-insensitive deduplication

    # Join into a cleaned sentence
    cleaned_phrase = " ".join(deduped)
    query = f'is {cleaned_phrase} true?'

    return query