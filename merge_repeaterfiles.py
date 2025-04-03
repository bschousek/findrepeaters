import pandas as pd
import glob

# Define the directory containing the CSV files (adjust as needed)
directory = "."

# Find all CSV files starting with "rb_" in the directory
csv_files = glob.glob(f"{directory}/rb_*.csv")

# Load and merge CSV files
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged data as data.csv
merged_df.to_csv("data.csv", index=False)

print(f"Merged {len(csv_files)} files into data.csv successfully!")
