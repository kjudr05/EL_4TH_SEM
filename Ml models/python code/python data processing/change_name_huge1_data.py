import pandas as pd
import ast
import re
import random
import spacy
from multiprocessing import freeze_support

def main():
    # 1) Load spaCy with ONLY the NER component
    nlp = spacy.load(
        "en_core_web_sm",
        disable=["parser", "tagger", "lemmatizer", "attribute_ruler"]
    )

    # 2) Pool of Indian names
    indian_names = [
        "Amit Sharma","Priya Singh","Rohit Verma","Neha Gupta","Sanjay Patel",
        "Pooja Mehta","Vikas Jain","Anjali Yadav","Rajiv Chauhan","Shreya Khanna",
        "Ajay Kapoor","Kavita Rao","Deepak Bansal","Sunita Das","Arun Malhotra",
        "Nisha Sethi","Arjun Reddy","Sneha Nair","Vishnu Kumar","Lakshmi Menon",
        "Mukesh Reddy","Divya Pillai","Pradeep Nair","Meera Iyer","Suresh Gowda",
        "Anitha Reddy","Manoj Prasad","Nandini Shetty","Mohammed Khan",
        "Aisha Siddiqui","Imran Ahmed","Fatima Begum","Salman Ali","Zara Sheikh",
        "Asif Qureshi","Mariam Syed","Rizwan Hussain","Sana Mirza","Nadeem Raza",
        "Sana Khan","Ibrahim Pasha","Zeenat Banu","Farhan Ahmed","Rukhsana Bi",
        "Shahid Rizvi","Parveen Fatima","Naveed Basha","Sabina Unnisa",
        "Harpreet Singh","Gurpreet Kaur","Manpreet Singh","Jasleen Kaur",
        "Kuldeep Singh","Simran Kaur","Balwinder Singh","Preeti Kaur",
        "Joseph D’Souza","Anita Fernandes","George Thomas","Mary George",
        "Michael Rodrigues","Sharon Pereira","David Fernandes","Priya D’Mello",
        "Mahesh Shah","Sunita Mehta","Tenzin Norbu","Dolma Lama","Lakha Bhil",
        "Kavita Munda","Raju Santhal","Phoolmati Oraon","Arunava Banerjee",
        "Soma Roy","Rahul Chatterjee","Madhuri Das","Sourav Bose","Anuradha Sinha",
        "Rina Patnaik","Pradeep Ghosh","Jayesh Shah","Meenal Desai","Sachin Deshmukh",
        "Snehal Kulkarni","Neeraj Kumar","Ankita Sharma","Rajan Gupta","Shalini Verma",
        "Vivek Kumar","Swati Singh","Karan Mehta","Sonal Jain","Nikhil Patel",
        "Richa Sharma","Aarav Desai","Isha Khurana","Devendra Yadav","Bhavna Batra",
        "Raghav Sood","Megha Chopra","Anand Roy","Tara Sen","Abdul Rahman",
        "Rekha Nair","Kunal Bhatia","Ritu Shah","Faizal Ahmed","Surbhi Grover",
        "Vijay Pillai","Maya Prasad","Rohini Kadam","Vipin Rawat","Zubair Khan",
        "Laila Farooqi","Dhruv Agarwal","Renuka Patil","Imtiyaz Sheikh",
        "Shaila Bhattacharya","Jatin Malhotra","Rhea Roy","Aslam Khan",
        "Shubha Reddy","Fareed Ansari","Nidhi Saxena","Kabir Siddiqui",
        "Swara Bose","Harish Deshpande","Greeta Pereira","Rakesh Rao",
        "Leena Fernandes","Brijesh Mehta","Poonam Nandan"
    ]

    # 3) Load and parse
    df = pd.read_csv('huge1_final.csv', dtype=str)
    df['utterances'] = df['contents'].apply(ast.literal_eval)

    # 4) Flatten utterances and run NER in parallel
    conv_sizes = [len(c) for c in df['utterances']]
    flat_utts = [utt for conv in df['utterances'] for utt in conv]
    docs = list(nlp.pipe(flat_utts, batch_size=1000, n_process=2))

    # 5) Replace each PERSON with a random Indian name
    total = len(docs)
    ten_pct = max(1, total // 10)
    flat_replaced = []
    for i, doc in enumerate(docs, 1):
        text = doc.text
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                rnd = random.choice(indian_names)
                text = re.sub(rf"\b{re.escape(ent.text)}\b", rnd, text)
        flat_replaced.append(text)
        if i % ten_pct == 0 or i == total:
            print(f"Processed {i}/{total} utterances ({(i/total)*100:.0f}%)")

    # 6) Re-chunk and save
    out_chunks = []
    idx = 0
    for size in conv_sizes:
        out_chunks.append(flat_replaced[idx:idx+size])
        idx += size

    df['contents_indian'] = out_chunks
    df[['contents_indian','labels']].to_csv('changed_name_final.csv', index=False)
    print("Done: changed_name_final.csv")

if __name__ == '__main__':
    freeze_support()
    main()
