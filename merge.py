import pandas as pd
big_df = pd.read_csv("BB-raw.csv")
small_df = pd.read_csv("BB-daily-update.csv")
merged_df = pd.concat([big_df, small_df], ignore_index=True)
merged_df.to_csv("updated_big_file.csv", index=False)

