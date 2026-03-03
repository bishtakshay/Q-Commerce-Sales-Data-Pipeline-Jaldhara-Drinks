import pandas as pd

#BLINKIT DOWNLOADED FILE CLEANING

df_blinkit_raw = pd.read_csv('Existing Files/blinkit-raw.csv',low_memory=False)
df_blinkit_raw = df_blinkit_raw.drop('Internal SKU', axis = 1)

df_blinkit_raw = df_blinkit_raw[['item_id','item_name','manufacturer_id','manufacturer_name','city_id','city_name','category','date','qty_sold','mrp']]
print(df_blinkit_raw.iloc[[220035]])
df_blinkit_raw = df_blinkit_raw.drop(220035)

#stripping extra spaces(if present) from every column
for col in df_blinkit_raw.select_dtypes(include = 'object'):
    df_blinkit_raw[col] = df_blinkit_raw[col].str.strip()
    df_blinkit_raw[col] = df_blinkit_raw[col].astype('string')


df_blinkit_raw['item_id'] = pd.to_numeric(df_blinkit_raw['item_id'])
df_blinkit_raw['manufacturer_id'] = pd.to_numeric(df_blinkit_raw['manufacturer_id'])
df_blinkit_raw['city_id'] = pd.to_numeric(df_blinkit_raw['city_id'])
df_blinkit_raw['qty_sold'] = pd.to_numeric(df_blinkit_raw['qty_sold'])
df_blinkit_raw['mrp'] = pd.to_numeric(df_blinkit_raw['mrp'])
df_blinkit_raw['date'] = pd.to_datetime(df_blinkit_raw['date'],dayfirst=True)

df_blinkit_raw = df_blinkit_raw.drop_duplicates()
df_blinkit_raw.sort_values('date', inplace = True)

print(df_blinkit_raw.dtypes)
print(df_blinkit_raw.head())

df_blinkit_raw.to_csv("Output-files/blinkit_raw.csv", index = False)
