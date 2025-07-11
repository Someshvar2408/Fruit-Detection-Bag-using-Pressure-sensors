# -*- coding: utf-8 -*-
"""Preprocessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K1NnawW9hKilBitps8Qh_oWLC1yDZHzX
"""

import pandas as pd
import os
import glob
from scipy.stats import zscore

# Directory where CSV files are stored
data_dir = "fruit_csvs"  # <-- put your CSV files here
output_file = "merged_test.csv"

def clean_and_label_csv(file_path):
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        # Extract label from filename
        base_name = os.path.basename(file_path)
        label = base_name.split('.')[0].split('_')[0].lower()  # e.g., "apple_data.csv" -> "apple"
        df["Label"] = label

        return df

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    all_dfs = []

    for file in all_files:
        print(f"Processing: {file}")
        cleaned_df = clean_and_label_csv(file)
        if cleaned_df is not None and not cleaned_df.empty:
            all_dfs.append(cleaned_df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"\n✅ Cleaned and merged data saved to: {output_file}")
        print(f"Total samples: {len(combined_df)}")
        print("Unique labels found:", combined_df['Label'].unique())
    else:
        print("❌ No valid data files found or all were empty after cleaning.")

if __name__ == "__main__":
    main()