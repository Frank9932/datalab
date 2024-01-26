import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import oracledb
import sys
import time
from datetime import datetime
from mod_functions import mod_load_config


formatted_time = datetime.fromtimestamp(time.time())
yea = formatted_time.year
mon = formatted_time.month
day = formatted_time.day
hour = formatted_time.hour
minute = formatted_time.minute


htmp_tmstmp = f"{yea}-{mon}-{day}-{hour}-{minute}"
htmp_title = f"HOTMAP  {htmp_tmstmp}"

mod_config = mod_load_config()
connection=oracledb.connect(
     config_dir= mod_config["wallet_dir"],
     user=mod_config["oracle_user"],
     password=mod_config["oracle_password"],
     dsn = mod_config["dsn"],
     wallet_location=mod_config["wallet_location"],
     wallet_password=mod_config["wallet_password"])

cursor = connection.cursor()

tn = mod_config["table_name"]
sql = f"SELECT TO_CHAR(ut, 'YYYY-MM-DD HH24:MI:SS') AS formatted_ut, symList FROM {tn}"
cursor.execute(sql)
df = pd.read_sql(sql,connection)

connection.close()

df["SYMLIST"] = df["SYMLIST"].transform(eval)

symPool = [i[1] for sublist in df['SYMLIST'].values for i in sublist]
unique_values = np.unique(symPool).tolist()

dfhtmp = pd.DataFrame(columns=['timestamp'] + unique_values)
dfhtmp["timestamp"] = df["FORMATTED_UT"]
dfhtmp["timestamp"] = pd.to_datetime(df["FORMATTED_UT"])

cols = dfhtmp.columns
inum = 1
while inum < len(cols) :
    sym = cols[inum]
    for index, row in df.iterrows():
        for pair in row[1]:
            if pair[1] == sym :
                dfhtmp.iloc[index,inum] = pair[0]
    inum += 1 
    
dfhtmp.set_index("timestamp", inplace=True)
dfhtmp = dfhtmp.sort_values(by='timestamp')
dfhtmp = dfhtmp.fillna(0.0)
ddf= dfhtmp.describe()
ddfstd = ddf.sort_values(by='mean',axis='columns')

dfhtmp_reordered = dfhtmp.reindex(columns=ddfstd.columns)
dfhtmp_ds = dfhtmp_reordered.describe()
df_max = dfhtmp_ds.loc['max'].max()
df_min = dfhtmp_ds.loc['max'][dfhtmp_ds.loc['max'] != 0].min()

sns.color_palette("mako", as_cmap=True)
plt.figure(figsize=(100, 40))
plt.title(htmp_title)


sns.heatmap(dfhtmp_reordered.T, annot=False, fmt=".6f", vmin = df_min, vmax = df_max, linewidths=.05, cbar_kws={'label': 'Your Colorbar Label'})
plt.savefig(f"hotmap-{htmp_tmstmp}.png")
print(f"HOTMAP {yea}-{mon}-{day}-{hour}-{minute}.png SAVED")


