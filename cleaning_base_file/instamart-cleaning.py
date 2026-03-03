import pandas as pd

#Instamart DOWNLOADED FILE CLEANING

df_instamart_raw = pd.read_csv('Existing Files/instamart-raw.csv',low_memory=False)

#dropping useless columns
print(df_instamart_raw.info())
df_instamart_raw.drop(df_instamart_raw.iloc[:,0:11], axis = 1, inplace = True)

#stripping extra spaces(if present) from every column
for col in df_instamart_raw.select_dtypes(include = 'object'):
    df_instamart_raw[col] = df_instamart_raw[col].str.strip()
    df_instamart_raw[col] = df_instamart_raw[col].astype('string')

df_instamart_raw.rename(columns = {"GMV.1":"GMV"}, inplace = True)

df_instamart_raw['ORDERED_DATE'] = pd.to_datetime(df_instamart_raw['ORDERED_DATE'], dayfirst = True, format = 'mixed')
df_instamart_raw.sort_values("ORDERED_DATE", inplace = True)

print(df_instamart_raw.info())

df_instamart_raw.to_csv("Output-files/instamart_raw.csv", index = False)