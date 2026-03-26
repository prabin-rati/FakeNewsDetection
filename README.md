# Fake News Detection System
**BCA 6th Semester - Project II (TU)**

## 📌 Project Overview
A Machine Learning-based web application that classifies news articles as 'Real' or 'Fake' using Natural Language Processing (NLP).

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **ML Model:** Passive Aggressive Classifier
- **Vectorization:** TfidfVectorizer
- **Web Framework:** Streamlit
- **IDE:** VS Code (macOS)

## 📂 Folder Structure
- `data/`: Contains the news dataset (CSV).
- `models/`: Saved `.pkl` files for the model and vectorizer.
- `app.py`: The Streamlit frontend code.
- `train_model.py`: Script to train the ML model.

## 🚀 How to Run
1. Activate Virtual Env: `source venv/bin/activate`
2. Install Dependencies: `pip install -r requirements.txt`
3. Run App: `streamlit run app.py`