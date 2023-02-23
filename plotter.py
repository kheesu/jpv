import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 600
mpl.rcParams['font.size'] = 7


def str_to_datetime(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')

filename = input('Enter the name of the file to plot : ')

file = open(filename)

data = json.load(file)

#TODO: use try except to catch files with invalid format
dat0 = data['DiagnosticData']['LFPTrendLogs']['HemisphereLocationDef.Left']

cnt = 0
arr = [[], []]

for i in dat0:
    for j in dat0[i]:
        arr[0].append(str_to_datetime(j['DateTime']))
        arr[1].append(j['LFP'])

d = {'time':arr[0], 'LFP':arr[1]}
df = pd.DataFrame(data=d)

df.sort_values(by='time', inplace=True)

plt.plot(df['time'], df['LFP'])
plt.savefig('wholeplot.png')

starttime = input('Enter the start of the range of date to display in the format of YYYY-MM-DD: ')
endtime = input('Enter the end of the range of date to display in the format of YYYY-MM-DD: ')

df['time'] = pd.to_datetime(df['time'])
mask = (df['time'] > starttime) & (df['time'] <= endtime)

newdf = df.loc[mask]
plt.plot(newdf['time'], newdf['LFP'])
plt.savefig('rangeplot.png')