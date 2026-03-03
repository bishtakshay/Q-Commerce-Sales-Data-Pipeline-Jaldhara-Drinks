import pandas as pd

#BIG BASKET DOWNLOADED FILE CLEANING

df_bigbasket_raw = pd.read_csv('Existing Files/big-basket-raw.csv',low_memory=False)

for col in df_bigbasket_raw.select_dtypes(include = "object"):
    df_bigbasket_raw[col] = df_bigbasket_raw[col].str.strip()
    df_bigbasket_raw[col] = df_bigbasket_raw[col].astype('string')

df_bigbasket_raw.drop(df_bigbasket_raw.iloc[:,0:10], axis = 1, inplace = True)

df_bigbasket_raw['start_date'] = pd.to_datetime(df_bigbasket_raw['date_range'].str.slice(0,8), format = "%Y%m%d", errors = "coerce")
df_bigbasket_raw['end_date'] = pd.to_datetime(df_bigbasket_raw['date_range'].str.slice(-8), format = "%Y%m%d", errors = "coerce")

df_bigbasket_raw = df_bigbasket_raw[['start_date','end_date','date_range','source_city_name','brand_name',
                                     'top_slug','mid_slug','leaf_slug','source_sku_id','sku_description',
                                     'sku_weight','total_quantity','total_mrp','total_sales']]

print(df_bigbasket_raw.info())
print(df_bigbasket_raw.head())

df_bigbasket_raw.to_csv("Output-files/bigbasket_raw.csv", index = False)