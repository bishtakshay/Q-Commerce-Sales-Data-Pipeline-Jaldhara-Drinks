# ============================================================
# DATA CLEANING SCRIPT — Q-COMMERCE RAW FILES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ── PATHS ────────────────────────────────────────────────────

INPUT_DIR  = "Existing Files"
OUTPUT_DIR = "Output-files"


# ============================================================
# 1. BLINKIT
# ============================================================

df_blinkit = pd.read_csv(f"{INPUT_DIR}/blinkit-raw.csv", low_memory=False)

df_blinkit.drop(columns=["Internal SKU"], inplace=True)
df_blinkit = df_blinkit[["item_id", "item_name", "manufacturer_id", "manufacturer_name",
                          "city_id", "city_name", "category", "date", "qty_sold", "mrp"]]
df_blinkit.drop(index=220035, inplace=True)

for col in df_blinkit.select_dtypes(include="object"):
    df_blinkit[col] = df_blinkit[col].str.strip().astype("string")

df_blinkit["item_id"]         = pd.to_numeric(df_blinkit["item_id"])
df_blinkit["manufacturer_id"] = pd.to_numeric(df_blinkit["manufacturer_id"])
df_blinkit["city_id"]         = pd.to_numeric(df_blinkit["city_id"])
df_blinkit["qty_sold"]        = pd.to_numeric(df_blinkit["qty_sold"])
df_blinkit["mrp"]             = pd.to_numeric(df_blinkit["mrp"])
df_blinkit["date"]            = pd.to_datetime(df_blinkit["date"], dayfirst=True)

df_blinkit.drop_duplicates(inplace=True)
df_blinkit.sort_values("date", inplace=True)

df_blinkit.to_csv(f"{OUTPUT_DIR}/blinkit_raw.csv", index=False)


# ============================================================
# 2. ZEPTO
# ============================================================

df_zepto = pd.read_csv(f"{INPUT_DIR}/zepto-raw.csv", low_memory=False)

df_zepto.drop(df_zepto.iloc[:, 0:10], axis=1, inplace=True)
df_zepto.rename(columns={
    "Date.1"           : "date",
    "SKU Name"         : "sku_name",
    "SKU ID"           : "sku_id",
    "City.1"           : "city",
    "Brand Name"       : "brand_name",
    "Manufacturer ID"  : "manufacture_id",
    "Manufacturer Name": "manufacture_name",
    "SKU Category"     : "sku_category",
    "Quantity"         : "quantity",
    "GMV.1"            : "gmv",
}, inplace=True)

df_zepto["date"] = pd.to_datetime(df_zepto["date"].str.replace("-", "/"), dayfirst=True)

for col in df_zepto.select_dtypes(include="object"):
    df_zepto[col] = df_zepto[col].str.strip().astype("string")

df_zepto.dropna(subset=["quantity"], inplace=True)
df_zepto.sort_values("date", inplace=True)

df_zepto.to_csv(f"{OUTPUT_DIR}/zepto_raw.csv", index=False)


# ============================================================
# 3. INSTAMART
# ============================================================

df_instamart = pd.read_csv(f"{INPUT_DIR}/instamart-raw.csv", low_memory=False)

df_instamart.drop(df_instamart.iloc[:, 0:11], axis=1, inplace=True)

for col in df_instamart.select_dtypes(include="object"):
    df_instamart[col] = df_instamart[col].str.strip().astype("string")

df_instamart.rename(columns={"GMV.1": "GMV"}, inplace=True)
df_instamart["ORDERED_DATE"] = pd.to_datetime(df_instamart["ORDERED_DATE"], dayfirst=True, format="mixed")
df_instamart.sort_values("ORDERED_DATE", inplace=True)

df_instamart.to_csv(f"{OUTPUT_DIR}/instamart_raw.csv", index=False)


# ============================================================
# 4. FK MINUTES
# ============================================================

df_fkminutes = pd.read_csv(f"{INPUT_DIR}/fkminutes-raw.csv", low_memory=False)

df_fkminutes.drop(df_fkminutes.iloc[:, 0:11], axis=1, inplace=True)

for col in df_fkminutes.select_dtypes(include="object"):
    df_fkminutes[col] = df_fkminutes[col].str.strip().astype("string")

# Normalise date string and truncate to date part only
df_fkminutes["order_date_time"] = (
    df_fkminutes["order_date_time"]
    .str.replace("-", "/")
    .str[:10]
)
df_fkminutes["order_date_time"] = pd.to_datetime(df_fkminutes["order_date_time"], dayfirst=True, format="mixed")
df_fkminutes.sort_values("order_date_time", inplace=True)

df_fkminutes.to_csv(f"{OUTPUT_DIR}/fkminutes_raw.csv", index=False)


# ============================================================
# 5. BIG BASKET
# ============================================================

df_bigbasket = pd.read_csv(f"{INPUT_DIR}/big-basket-raw.csv", low_memory=False)

df_bigbasket.drop(df_bigbasket.iloc[:, 0:10], axis=1, inplace=True)

for col in df_bigbasket.select_dtypes(include="object"):
    df_bigbasket[col] = df_bigbasket[col].str.strip().astype("string")

# Big Basket provides a date range string (YYYYMMDD) — split into start and end dates
df_bigbasket["start_date"] = pd.to_datetime(df_bigbasket["date_range"].str[:8],  format="%Y%m%d", errors="coerce")
df_bigbasket["end_date"]   = pd.to_datetime(df_bigbasket["date_range"].str[-8:], format="%Y%m%d", errors="coerce")

df_bigbasket = df_bigbasket[["start_date", "end_date", "date_range", "source_city_name", "brand_name",
                              "top_slug", "mid_slug", "leaf_slug", "source_sku_id", "sku_description",
                              "sku_weight", "total_quantity", "total_mrp", "total_sales"]]

df_bigbasket.to_csv(f"{OUTPUT_DIR}/bigbasket_raw.csv", index=False)