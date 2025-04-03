import pandas as pd

# Load CSV file
df = pd.read_csv("omaha.csv")

# Remove duplicate rows
df_cleaned = df.drop_duplicates()

# Ensure the "Channel Number" column is properly reindexed
if "Channel Number" in df_cleaned.columns:
    df_cleaned["Channel Number"] = range(1, len(df_cleaned) + 1)

# Save the cleaned CSV file
df_cleaned.to_csv("omaha_cleaned.csv", index=False)

print("Duplicates removed and Channel Number reindexed! Cleaned file saved as omaha_cleaned.csv.")
