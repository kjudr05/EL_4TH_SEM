import pandas as pd
import spacy
import ast
from tqdm import tqdm

# Load spaCy without parser/tagger for speed
nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer", "attribute_ruler"])

# Load your CSV
df = pd.read_csv("huge2_final.csv", dtype=str)

# Convert 'contents' column back to list of utterances
df['utterances'] = df['contents'].apply(ast.literal_eval)

# Flatten utterances to process all texts at once
flat_texts = [utt for conv in df['utterances'] for utt in conv]

# Remove PERSON entities from each utterance
def remove_names(doc):
    chunks = []
    last = 0
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            chunks.append(doc.text[last:ent.start_char])
            last = ent.end_char
    chunks.append(doc.text[last:])
    return "".join(chunks)

# Process in batch using spaCy's pipe
print("Processing utterances...")
cleaned = []
for doc in tqdm(nlp.pipe(flat_texts, batch_size=1000), total=len(flat_texts)):
    cleaned.append(remove_names(doc))

# Reconstruct conversations
index = 0
new_convs = []
for conv in df['utterances']:
    n = len(conv)
    new_convs.append(cleaned[index:index+n])
    index += n

# Add to DataFrame
df['contents_no_names'] = new_convs

# Save to CSV
df[['contents_no_names', 'labels']].to_csv("no_name_huge2.csv", index=False)

print("✅ Done. Output saved to cleaned_dataset.csv")
