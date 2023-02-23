#TODO: Change infile.txt to a folder where the files to be visualized goes in.

import os
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 600
mpl.rcParams['font.size'] = 7
#plt.rcParams['font.family'] = 'sans-serif'
#plt.rcParams['font.sans-serif'] = ['Arial']

def str_to_datetime(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')

def raw_to_dataframe(data):
    arr = [[], [], []]

    for i in data:
        for j in data[i]:
            arr[0].append(str_to_datetime(j['DateTime']))
            arr[1].append(j['LFP'])
            arr[2].append(str_to_datetime(j['DateTime']).date())
    
    d = {'time':arr[0], 'LFP':arr[1], 'date':arr[2]}
    df = pd.DataFrame(data=d)
    df.sort_values(by='time', inplace=True)
    return df

def print_fig(df, name):
    plt.plot(df['time'], df['LFP'])
    plt.savefig('pictures/' + name)
    plt.clf()

def print_two_figs(Ldf, Rdf, name):
    plt.plot(Ldf['time'], Ldf['LFP'], alpha=0.6)
    plt.plot(Rdf['time'], Rdf['LFP'], alpha=0.6)
    plt.savefig('pictures/both/' + name)
    plt.clf()

file = open('infiles.txt')
filenames = file.readlines()
filenames = [l.strip('\n\r') for l in filenames]

if not os.path.exists('pictures'):
    os.makedirs('pictures')
    os.makedirs('pictures/both')
    os.makedirs('pictures/left')
    os.makedirs('pictures/right')

if not os.path.exists('pictures/both'):
    os.makedirs('pictures/both')

if not os.path.exists('pictures/left'):
    os.makedirs('pictures/left')

if not os.path.exists('pictures/right'):
    os.makedirs('pictures/right')

for filename in filenames:

    rawfile = open(filename)

    data = json.load(rawfile)
    datL = data['DiagnosticData']['LFPTrendLogs']['HemisphereLocationDef.Left']
    datR = data['DiagnosticData']['LFPTrendLogs']['HemisphereLocationDef.Right']

    Ldf = raw_to_dataframe(datL)
    Rdf = raw_to_dataframe(datR)

    stripped_filename = filename.split('.')[0]

    print_fig(Ldf, '/left/LHEMI_ALL_' + stripped_filename + '.png')
    print_fig(Ldf, '/right/RHEMI_ALL_' + stripped_filename + '.png')
    print_two_figs(Ldf, Rdf, 'BOTH_ALL_' + stripped_filename + '.png')

    curday = Ldf.iloc[0][0].date()
    endday = Ldf.iloc[-1][0].date()
    
    while curday <= endday:
        dailyLdf = Ldf.loc[(Ldf['date'] == curday)]
        dailyRdf = Rdf.loc[(Rdf['date'] == curday)]

        print_fig(dailyLdf, '/left/LHEMI_' + str(curday) + '_' + stripped_filename + '.png')
        print_fig(dailyRdf, '/right/RHEMI_' + str(curday) + '_' + stripped_filename + '.png')
        print_two_figs(dailyLdf, dailyRdf, 'BOTH_' + str(curday) + '_' + stripped_filename + '.png')

        curday += timedelta(days=1)