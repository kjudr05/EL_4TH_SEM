import pandas as pd
import ast
import spacy
import re

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def remove_names(text):
    """
    Removes all named entities labeled as PERSON from a string.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Replace full name matches only
            pattern = r'\b{}\b'.format(re.escape(ent.text))
            text = re.sub(pattern, "[REDACTED]", text)
    return text

def clean_transcript_list(transcript_str):
    """
    Converts the stringified list to a Python list, removes names from each message, then returns a cleaned stringified list.
    """
    try:
        messages = ast.literal_eval(transcript_str)
        if isinstance(messages, list):
            cleaned = [remove_names(msg) for msg in messages]
            return str(cleaned)
    except Exception:
        pass
    return transcript_str  # Return unchanged if parsing fails

# Load the dataset
df = pd.read_csv("huge2_final.csv")

# Clean the transcript column
df['transcript'] = df['transcript'].apply(clean_transcript_list)

# Save to a new CSV file
df.to_csv("no_name_huge2.csv", index=False)

print("✅ Names removed and saved to 'change_name2_cleaned.csv'")
