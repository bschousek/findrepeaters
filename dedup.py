import pandas as pd

# Load base data and Omaha repeater list
df_base = pd.read_csv("bws_base.csv")
df_omaha = pd.read_csv("omaha.csv")

# Remove duplicates in Omaha data
df_omaha_cleaned = df_omaha.drop_duplicates()

# Merge base data with cleaned Omaha data (prepend `bws_base.csv`)
df_combined = pd.concat([df_base, df_omaha_cleaned], ignore_index=True)

# Ensure the "Channel Number" column is properly reindexed
if "Channel Number" in df_combined.columns:
    df_combined["Channel Number"] = range(1, len(df_combined) + 1)

# Save the final cleaned and merged CSV
df_combined.to_csv("omaha_cleaned.csv", index=False)

print("Base data prepended, duplicates removed, and channels renumbered! Saved as omaha_cleaned.csv.")
