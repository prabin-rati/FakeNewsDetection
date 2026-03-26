import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download the 'dictionary' of useless words
nltk.download('stopwords')
ps = PorterStemmer()

# --- NEW: Load the data first ---
fake = pd.read_csv('data/Fake.csv')
true = pd.read_csv('data/True.csv')

# Add labels and combine
fake['label'] = 0
true['label'] = 1
df = pd.concat([fake, true]).sample(frac=1).reset_index(drop=True)
# --------------------------------

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # 1. Remove everything except letters
    text = re.sub('[^a-zA-Z]', ' ', text)
    # 2. Lowercase and split
    text = text.lower().split()
    # 3. Remove stopwords and Stem
    text = [ps.stem(word) for word in text if not word in stopwords.words('english')]
    return ' '.join(text)

# Apply to your data
print("Cleaning data... This will take a few minutes. Do not close the terminal.")
df['text'] = df['text'].apply(clean_text)

# Save the final cleaned data
df.to_csv('data/final_cleaned_news.csv', index=False)
print("✅ Done! Your data is now ready for the ML model.")