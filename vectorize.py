from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

# 1. Load your cleaned data
df = pd.read_csv('data/final_cleaned_news.csv')
df = df.dropna() # Remove any empty rows

# 2. Initialize the Vectorizer
# max_features=5000 keeps the top 5000 most important words
tfidf = TfidfVectorizer(max_features=5000)

# 3. Transform the text into numbers (X)
X = tfidf.fit_transform(df['text']).toarray()

# 4. Get our labels (y)
y = df['label'].values

print(f"Feature matrix shape: {X.shape}") # Should be (Total Rows, 5000)

# 5. Save the vectorizer (Very Important for your Web App later!)
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
    
print("✅ Vectorizer saved as tfidf_vectorizer.pkl")