import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import oracledb
from sqlalchemy import create_engine

import sys
import time
from datetime import datetime

from mod_functions import mod_load_config

mod_config = mod_load_config()

def get_timestamp():
    formatted_time = datetime.fromtimestamp(time.time())
    yea = formatted_time.year
    mon = formatted_time.month
    day = formatted_time.day
    hour = formatted_time.hour
    minute = formatted_time.minute


    htmp_tmstmp = f"{yea}-{mon}-{day}-{hour}-{minute}"
    return htmp_tmstmp

connection=oracledb.connect(
     config_dir= mod_config["wallet_dir"],
     user=mod_config["oracle_user"],
     password=mod_config["oracle_password"],
     dsn = mod_config["dsn"],
     wallet_location=mod_config["wallet_location"],
     wallet_password=mod_config["wallet_password"])
tn = mod_config["table_name"]
sql = f"SELECT TO_CHAR(ut, 'YYYY-MM-DD HH24:MI') AS FORMATTED_UT, SYMLIST FROM {tn}"
try:
    df = pd.read_sql(sql,connection)
finally:
    connection.close()

df["SYMLIST"] = df["SYMLIST"].transform(eval)

df = df.sort_values(by='FORMATTED_UT')
df.reset_index(drop=True, inplace=True)

symPool = [i[1] for sublist in df['SYMLIST'].values for i in sublist]
unique_values = np.unique(symPool).tolist()

dfhtmp = pd.DataFrame(columns=['FORMATTED_UT'] + unique_values)
dfhtmp["FORMATTED_UT"] = df["FORMATTED_UT"]
dfhtmp["FORMATTED_UT"] = pd.to_datetime(df["FORMATTED_UT"])

cols = dfhtmp.columns
dfhtmp["FORMATTED_UT"] = df["FORMATTED_UT"] 

inum = 1
while inum < len(cols):
    sym = cols[inum]
    for index, row in df.iterrows():
        for pair in row[1]:
            if sym == pair[1]:
                dfhtmp.loc[index,sym] = pair[0]
    inum += 1
    
dfhtmp.set_index("FORMATTED_UT", inplace=True)
dfhtmp = dfhtmp.fillna(0.0)

ddf= dfhtmp.describe()
ddfstd = ddf.sort_values(by='mean',axis='columns')

dfhtmp_reordered = dfhtmp.reindex(columns=ddfstd.columns)
dfhtmp_ds = dfhtmp_reordered.describe()
df_max = dfhtmp_ds.loc['max'].max()
df_min = dfhtmp_ds.loc['max'][dfhtmp_ds.loc['max'] != 0].min()

htmp_tmstmp = get_timestamp()
htmp_title = f"HOTMAP  {htmp_tmstmp}"

sns.color_palette("mako", as_cmap=True)
plt.figure(figsize=(100, 40))
plt.title(htmp_title)
sns.heatmap(dfhtmp_reordered.T, annot=False, fmt=".0f", vmin = df_min, vmax = df_max, linewidths=.05, cbar_kws={'label': 'Your Colorbar Label'})
plt.savefig(f"hotmap-{htmp_tmstmp}.png")
print(f"HOTMAP {htmp_tmstmp} SAVED")