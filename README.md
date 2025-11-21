🚨 Fake App Detection System
A Lightweight Cybersecurity Tool to Identify Fake UPI Applications

Team: G4

📌 Overview

Fake UPI applications are increasingly used in India to scam users by imitating apps like PhonePe, GPay, Paytm, and BHIM.
These fake apps often look identical — same icon, similar name, and misleading developer details.

This project aims to detect such fake apps using simple metadata analysis and lightweight image hashing.

Built in 8 hours during a hackathon.

🛠️ Features
✔️ 1. Name Similarity Detection

Uses fuzzy string matching to compare suspicious app names with official app names.

✔️ 2. Icon Hash Comparison (pHash)

Generates perceptual hash signatures to detect copied or edited icons.

✔️ 3. Package & Developer Verification

Checks for unusual or mismatched package names and unknown developer identifiers.

✔️ 4. Risk Scoring System

Outputs High / Medium / Low risk based on combined signals.

✔️ 5. Streamlit UI

Clean neon-styled dashboard to visualize results.

✔️ 6. Evidence Kit Export

Generates a forensic-style report summarizing all detection indicators.

📂 Project Structure
Fake_App_Det/
│
├── data/
│   ├── official/       # Icons + metadata of official apps
│   ├── suspicious/     # Fake samples for testing
│
├── src/
│   ├── name_matcher.py
│   ├── icon_hasher.py
│   ├── package_checker.py
│   ├── risk_score.py
│
├── ui/
│   ├── app.py          # Streamlit dashboard
│
├── tests/
│
├── pipeline.py         # Main detection pipeline
└── README.md

🚀 How It Works
Step 1: Select the Target App Brand

Examples: PhonePe, GPay, Paytm, etc.

Step 2: Run Detection

Pipeline compares:

Fuzzy name similarity

Icon pHash difference

Package name structure

Developer identity

Step 3: View Results

Each suspicious app shows:

App name

Risk score

Highlighted reasons (icon mismatch, name similarity % etc.)

Step 4: Export Evidence Kit

A downloadable report with:

Metadata

Hash comparisons

Final risk scoring

⚠️ Constraints (Hackathon Limitations)

❌ No Play Store API access

❌ Very small dataset

❌ Manual icon & metadata collection

❌ No GPU or ML models allowed

❌ Only 8 hours to build full system

❌ Offline environment restrictions

🔻 Shortcomings

Not scalable to real Play Store apps

Not fully automated (manual dataset required)

Basic risk scoring logic

Limited accuracy due to small dataset

Prototype-level UI

No real-time monitoring

🔮 Future Enhancements

✔️ Play Store live scanning

✔️ ML-based anomaly detection

✔️ Cloud deployment

✔️ Android app

✔️ Auto-scraping of metadata & icons

▶️ Running the Project
1. Install Dependencies
pip install -r requirements.txt

2. Run Streamlit UI
streamlit run ui/app.py

3. Add your samples

Place your suspicious app metadata/icons inside:

data/suspicious/

👥 TEAM- G4

Thammisetty Jahnavi(1BF24CS317)- Data Collection
Nall Tejaswini(1BM24IC032)-Detection Engine
Putta Hanisha Reddy(1BF24CS236)-UI/UX
Panchangam Sathya Hamsini(1BF24CS208)-Integration & Testing

🏁 Conclusion

This project demonstrates a fast, lightweight proof-of-concept for identifying fake UPI apps using metadata and hashing techniques — all built under strict time and resource constraints.
