# tflite_model.py

import os
import re
import numpy as np
import pandas as pd
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

# 1) NLTK setup
nltk.download("punkt")
nltk.download("stopwords")

# 2) Load & preprocess
df = pd.read_csv("final_complete_dataset.csv", encoding="latin1").dropna(subset=["Transcript","labels"])
ps = PorterStemmer()
stops = set(stopwords.words("english"))

def transform_text(t: str) -> str:
    toks = re.findall(r"\b\w+\b", t.lower())
    return " ".join(ps.stem(w) for w in toks if w not in stops)

df["clean"] = df["Transcript"].map(transform_text)

# 3) TF‑IDF
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df["clean"]).toarray()
y = df["labels"].astype(int).values

# 4) Train NB
nb = RandomForestClassifier()
nb.fit(X, y)

# 5) Build Keras wrapper
w = (nb.feature_log_prob_[1] - nb.feature_log_prob_[0]).astype(np.float32)
b = (nb.class_log_prior_[1] - nb.class_log_prior_[0]).astype(np.float32)
inp = tf.keras.Input(shape=(X.shape[1],), dtype=tf.float32, name="tfidf_input")
out = tf.keras.layers.Dense(
    1,
    activation="sigmoid",
    kernel_initializer=tf.keras.initializers.Constant(w.reshape(-1,1)),
    bias_initializer=tf.keras.initializers.Constant(b),
    trainable=False,
    name="nb_dense"
)(inp)
model = tf.keras.Model(inp, out, name="nb_wrapper")

# 6) Export SavedModel (Keras 3 API)
export_dir = "assets/saved_nb_model"
os.makedirs(export_dir, exist_ok=True)
model.export(export_dir)       # <— use export() instead of save()

# 7) Convert to TFLite
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# 8) Write .tflite
os.makedirs("assets", exist_ok=True)
with open("assets/model.tflite", "wb") as f:
    f.write(tflite_model)

# 9) Save vectorizer for client preprocessing
# after you have fit your TfidfVectorizer tfidf
import json
tfidf_data = {
    # Cast all vocabulary_ values (NumPy ints) into Python ints:
    "vocabulary": { token: int(index) 
                    for token, index in tfidf.vocabulary_.items() },
    # idf_.tolist() is already a list of Python floats
    "idf": tfidf.idf_.tolist()
}

with open("assets/vectorizer.json", "w") as f:
    json.dump(tfidf_data, f)

print("✅ Export complete: assets/model.tflite + assets/vectorizer.pkl")
