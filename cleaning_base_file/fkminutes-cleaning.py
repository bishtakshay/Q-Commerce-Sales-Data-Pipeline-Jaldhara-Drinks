import pandas as pd

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
