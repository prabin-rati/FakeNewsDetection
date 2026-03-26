import pandas as pd
import os

# 1. Check if the folder and files exist
data_dir = 'data'
fake_path = os.path.join(data_dir, 'Fake.csv')
true_path = os.path.join(data_dir, 'True.csv')

if os.path.exists(fake_path) and os.path.exists(true_path):
    print("✅ Files found in the /data folder!")
    
    # 2. Try loading a few rows to check for errors
    try:
        fake_df = pd.read_csv(fake_path, nrows=5)
        true_df = pd.read_csv(true_path, nrows=5)
        print("✅ Success! Pandas can read the CSV files.")
        print("\n--- Fake News Sample ---")
        print(fake_df[['title']].head(2))
    except Exception as e:
        print(f"❌ Error reading files: {e}")
else:
    print("❌ Files NOT found. Check your folder naming.")