import pandas as pd

#ZEPTO DOWNLOADED FILE CLEANING

df_zepto_raw = pd.read_csv('Existing Files/zepto-raw.csv',low_memory=False)

df_zepto_raw.drop(df_zepto_raw.iloc[:,0:10], axis = 1, inplace = True)

df_zepto_raw.rename(columns = {"Date.1":"date", 
                               "SKU Name":"sku_name",
                               "SKU ID":"sku_id",
                               "City.1":"city",
                               "Brand Name":
                               "brand_name",
                               "Manufacturer ID":"manufacture_id",
                               "Manufacturer Name":"manufacture_name",
                               "SKU Category":"sku_category",
                               "Quantity":"quantity",
                               "GMV.1":"gmv"}, inplace = True)

#changing date column from object to str
df_zepto_raw["date"] = df_zepto_raw["date"].str.replace("-", "/")
df_zepto_raw["date"] = pd.to_datetime(df_zepto_raw["date"], dayfirst=True)

#stripping extra spaces(if present) from every column
for col in df_zepto_raw.select_dtypes(include = 'object'):
    df_zepto_raw[col] = df_zepto_raw[col].str.strip()
    df_zepto_raw[col] = df_zepto_raw[col].astype('string')

df_zepto_raw.sort_values('date', inplace = True)
df_zepto_raw.dropna(subset=['quantity'], axis = 0, inplace = True)

print(df_zepto_raw.info())
print(df_zepto_raw.head())

df_zepto_raw.to_csv("Output-files/zepto_raw.csv", index = False)