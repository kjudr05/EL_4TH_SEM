import pandas as pd
import spacy

# 1) Load spaCy with only the NER component
nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer", "attribute_ruler"])

def strip_names(text: str) -> str:
    """
    Remove all PERSON entities from the input string.
    """
    if not isinstance(text, str):
        return text
    doc = nlp(text)
    result = []
    last_idx = 0
    # Iterate entities in document order
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # keep text before the name
            result.append(text[last_idx:ent.start_char])
            # skip the name
            last_idx = ent.end_char
    # append remainder
    result.append(text[last_idx:])
    return "".join(result)

def main():
    # 2) Load your CSV
    df = pd.read_csv("correct1.csv", dtype=str)

    # 3) Apply name-stripping to the transcript column
    df["transcript"] = df["transcript"].apply(strip_names)

    # 4) Save cleaned file
    df.to_csv("data_cleaned.csv", index=False)
    print("✅ Done! Cleaned data saved as data_cleaned.csv")

if __name__ == "__main__":
    main()
