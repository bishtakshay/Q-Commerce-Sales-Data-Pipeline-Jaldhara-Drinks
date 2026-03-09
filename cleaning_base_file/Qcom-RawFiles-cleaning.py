import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#BLINKIT DOWNLOADED FILE CLEANING

df_blinkit_raw = pd.read_csv('Existing Files/blinkit-raw.csv',low_memory=False)
df_blinkit_raw = df_blinkit_raw.drop('Internal SKU', axis = 1)

df_blinkit_raw = df_blinkit_raw[['item_id','item_name','manufacturer_id','manufacturer_name','city_id','city_name','category','date','qty_sold','mrp']]
#print(df_blinkit_raw.iloc[[220035]])
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

#print(df_blinkit_raw.dtypes)
#print(df_blinkit_raw.head())

df_blinkit_raw.to_csv("Output-files/blinkit_raw.csv", index = False)


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



#FKMinutes DOWNLOADED FILE CLEANING

df_fkminutes_raw = pd.read_csv('Existing Files/fkminutes-raw.csv',low_memory=False)

#dropping useless columns
df_fkminutes_raw.drop(df_fkminutes_raw.iloc[:,0:11], axis = 1, inplace = True)

#stripping extra spaces(if present) from every column
for col in df_fkminutes_raw.select_dtypes(include = 'object'):
    df_fkminutes_raw[col] = df_fkminutes_raw[col].str.strip()
    df_fkminutes_raw[col] = df_fkminutes_raw[col].astype('string')


print(f"The count of 1st row is {df_fkminutes_raw['order_date_time'].count()}")

df_fkminutes_raw['order_date_time'] = df_fkminutes_raw['order_date_time'].str.replace("-","/")
df_fkminutes_raw['order_date_time'] = df_fkminutes_raw['order_date_time'].str[:10]

df_fkminutes_raw['order_date_time'] = pd.to_datetime(df_fkminutes_raw['order_date_time'], dayfirst= True, format='mixed')

df_fkminutes_raw.sort_values("order_date_time", inplace= True)

print(df_fkminutes_raw.head(5))
print(df_fkminutes_raw.info())

df_fkminutes_raw.to_csv("Output-files/fkminutes_raw.csv", index = False)



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