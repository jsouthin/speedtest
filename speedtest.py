import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
pd.options.mode.chained_assignment = None  # default='warn'

logfile    = "/home/pi/Projects/speedtest/speedtest.log"
chart_file = "/home/pi/Projects/speedtest/speedtest.png"

df = pd.read_table(logfile, header=None)
# you might need to update this if you have a slightly different setup that I do

df['time'] = df[0].apply(lambda x: x.split("[")[1].split("]")[0])
df['message'] = df[0].apply(lambda x: x.split("]")[1])

dl = df[df['message'].str.contains('Download')]
ul = df[df['message'].str.contains('Upload')]
ul['upload speed'] = ul['message'].apply(lambda x: x.split(" ")[2])
dl['download speed'] = dl['message'].apply(lambda x: x.split(" ")[2])
out = dl[['time','download speed']].merge(ul[['time','upload speed']])

out['time'] = pd.to_datetime(out['time'])
out['download speed'] = out['download speed'].astype(float)
out['upload speed'] = out['upload speed'].astype(float)
out['date'] = out['time'].dt.floor("D")

qt90 = out.groupby(pd.Grouper(key='time',freq='D')).quantile(q=0.9).reset_index().drop('time',axis=1)
qt50 = out.groupby(pd.Grouper(key='time',freq='D')).quantile(q=0.5).reset_index().drop('time',axis=1)
qt10 = out.groupby(pd.Grouper(key='time',freq='D')).quantile(q=0.1).reset_index().drop('time',axis=1)

out = out.merge(qt90, how='inner', on='date').rename(columns={"download speed_x": "download speed", "upload speed_x": "upload speed","download speed_y":"p90 download","upload speed_y":"p90 upload"})

out = out.merge(qt10, how='inner', on='date').rename(columns={"download speed_x": "download speed", "upload speed_x": "upload speed","download speed_y":"p10 download","upload speed_y":"p10 upload"})

out = out.merge(qt50, how='inner', on='date').drop('date',axis=1).rename(columns={"download speed_x": "download speed", "upload speed_x": "upload speed","download speed_y":"p50 download","upload speed_y":"p50 upload"})

out['rolling dl'] = out['download speed'].rolling(window=12).mean()

fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(out.time, out['download speed'], label='Download', marker='.', s=1, alpha = 0.5)
ax.scatter(out.time, out['upload speed'] , label='Upload', marker = '.', s=1, alpha = 0.5)
ax.plot(out.time, out['p50 download'], linestyle='--',linewidth=0.5, label='p50 download')
ax.plot(out.time, out['p50 upload'], linestyle='--',linewidth=0.5, label='p50 upload')
ax.plot(out.time, out['p10 download'], linestyle='--',linewidth=0.5, label='p90 download')
ax.plot(out.time, out['p10 upload'], linestyle='--',linewidth=0.5, label='p90 upload')
ax.plot(out.time, out['rolling dl'] ,linewidth=1, label='rolling 1hr m.a. dl')
ax.axhline(y=34,linestyle='dotted',linewidth=2,c='grey',label="Stay Fast Guarantee = 34 Mbps", alpha = 0.5)
ax.set_title("Speedtest.net internet speeds")
ax.set_xlabel("Datetime")
ax.set_ylabel("Mbps")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
plt.xticks(rotation=90)
#ax.set_ylim(4,40)
#ax.set_yscale('log')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig(chart_file, dpi=300, bbox_inches = "tight")