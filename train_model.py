import pandas as pd
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import os

# 1. Create models folder if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# 2. Load the cleaned data
print("Reading cleaned data...")
try:
    df = pd.read_csv('data/final_cleaned_news.csv')
    # Drop any rows that became empty during cleaning
    df.dropna(subset=['text'], inplace=True)
except FileNotFoundError:
    print("❌ Error: 'data/final_cleaned_news.csv' not found. Please run clean_data.py first!")
    exit()

# 3. Initialize Vectorizer
print("Vectorizing text... this may take a moment.")
tfidf_v = TfidfVectorizer(max_features=5000, ngram_range=(1,3))
X = tfidf_v.fit_transform(df['text'])
y = df['label']

# 4. Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the Model
print("Training the model...")
model = PassiveAggressiveClassifier(max_iter=50)
model.fit(X_train, y_train)

# 6. Check Accuracy
y_pred = model.predict(X_test)
score = accuracy_score(y_test, y_pred)
print(f"✅ Training Complete! Accuracy: {round(score*100, 2)}%")

# 7. SAVE BOTH FILES TO THE MODELS FOLDER
print("Saving files to 'models/' folder...")

with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_v, f)

print("🚀 Success! Both 'model.pkl' and 'tfidf_vectorizer.pkl' are ready.")