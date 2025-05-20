import pandas as pd
from sklearn.utils import shuffle

# Load all CSV files
df1 = pd.read_csv("huge1_final.csv")
df2 = pd.read_csv("huge2_final.csv")
df3 = pd.read_csv("correct.csv")

# Combine all dataframes
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# Shuffle the combined dataframe
shuffled_df = shuffle(combined_df, random_state=42)

# Save to a new CSV file
shuffled_df.to_csv("combined_shuffled_final.csv", index=False)
