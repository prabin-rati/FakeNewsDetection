import pandas as pd

# 1. Load the data
fake_df = pd.read_csv('data/Fake.csv')
true_df = pd.read_csv('data/True.csv')

# 2. Add labels (0 for Fake, 1 for True)
fake_df['label'] = 0
true_df['label'] = 1

# 3. Combine them into one single dataframe
df = pd.concat([fake_df, true_df], axis=0).reset_index(drop=True)

# 4. Remove unnecessary columns to keep it fast
# Usually, we only need 'text' (or 'title') and 'label'
df = df[['text', 'label']]

# 5. Shuffle the data (important so the model doesn't see all fake then all true)
df = df.sample(frac=1).reset_index(drop=True)

print(f"Total rows in combined dataset: {len(df)}")
print(df.head())

# 6. Save the cleaned version for training later
df.to_csv('data/combined_news.csv', index=False)
print("✅ Combined dataset saved to data/combined_news.csv")