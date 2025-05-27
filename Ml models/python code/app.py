import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# --- Preprocess ---
ps = PorterStemmer()
stopwords_set = set(stopwords.words("english"))
def transform_text(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    filtered = [ps.stem(word) for word in tokens if word not in stopwords_set]
    return " ".join(filtered)



# --- Load models ---
tfidf = pickle.load(open('Ml models/pkl format/vectorizer.pkl', 'rb'))
model = pickle.load(open('Ml models/pkl format/model.pkl', 'rb'))

# --- Page setup ---
st.set_page_config(page_title="Spam Classifier", layout="wide", page_icon="📨")

# --- Hide Streamlit default header/footer & remove top padding ---
st.markdown("""
    <style>
    /* Hide menu & footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* Remove all default top padding so header sits flush */
    .block-container { padding-top: 0rem; max-width: 800px; margin: auto; }

    /* Glassmorphism container */
    .container {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 2.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Fonts & background */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #fff;
    }

    /* Header styling */
    .title {
        font-size: 2.8rem;
        color: #ff4b2b;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #ccc;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }

    /* Text area */
    textarea {
        background: #1a1a1a !important;
        color: #f5f5f5 !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }

    /* Button */
    .stButton>button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        background: linear-gradient(135deg, #ff4b2b, #ff416c);
    }

    /* Result box */
    .result {
        margin-top: 1.5rem;
        padding: 1rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        border-radius: 12px;
    }
    .spam { background: #c62828; }
    .ham  { background: #2e7d32; }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        color: #888;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Build UI ---
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown('<div class="title">📨 SCAM Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter/Paste a Call Transcript below and let AI tell you if it was a SCAM or NOT SCAM.</div>', unsafe_allow_html=True)

input_sms = st.text_area("🔤 Your message here:")

if st.button("🚀 Check Spam"):
    transformed = transform_text(input_sms)
    vect = tfidf.transform([transformed])
    pred = model.predict(vect)[0]

    if pred == 1:
        st.markdown('<div class="result spam">🚨 This is SCAM</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result ham">✅ Not SCAM</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Developed by Ibrahim & Team</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)