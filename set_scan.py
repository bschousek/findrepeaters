import pandas as pd

# Load the cleaned CSV file
df = pd.read_csv("omaha_cleaned.csv")

# Check if 'Skip' column exists, then update it
if "Skip" in df.columns:
    df["Skip"] = "Select"

    # Save the updated CSV file
    df.to_csv("omaha_cleaned_updated.csv", index=False)
    print("All values in the 'Skip' column set to 'Select'! Saved as omaha_cleaned_updated.csv.")
else:
    print("Error: 'Skip' column not found in the CSV.")
