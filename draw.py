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
    plt.xlabel('Time')
    plt.ylabel('LFP')
    plt.plot(df['time'], df['LFP'])
    plt.savefig(os.path.join('pictures', name))
    plt.clf()

def print_two_figs(Ldf, Rdf, name):
    plt.xlabel('Time')
    plt.ylabel('LFP')
    plt.plot(Ldf['time'], Ldf['LFP'], alpha=0.6, label='Left')
    plt.plot(Rdf['time'], Rdf['LFP'], alpha=0.6, label='Right')
    plt.legend()
    plt.savefig(os.path.join('pictures', 'both', name))
    plt.clf()

filenames = [os.path.join('infiles/', f) for f in os.listdir('infiles/') if os.path.isfile(os.path.join('infiles/', f))]

"""
file = open('infiles.txt')
filenames = file.readlines()
filenames = [l.strip('\n\r') for l in filenames]
filenames = list(filter(None, filenames))
"""

if not os.path.exists('pictures'):
    os.makedirs('pictures')
    os.makedirs(os.path.join('pictures', 'both'))
    os.makedirs(os.path.join('pictures', 'left'))
    os.makedirs(os.path.join('pictures', 'right'))

if not os.path.exists('pictures/both'):
    os.makedirs(os.path.join('pictures', 'both'))

if not os.path.exists('pictures/left'):
    os.makedirs(os.path.join('pictures', 'left'))

if not os.path.exists('pictures/right'):
    os.makedirs(os.path.join('pictures', 'right'))

for filename in filenames:

    rawfile = open(filename)

    data = json.load(rawfile)
    try:
        datL = data['DiagnosticData']['LFPTrendLogs']['HemisphereLocationDef.Left']
        datR = data['DiagnosticData']['LFPTrendLogs']['HemisphereLocationDef.Right']
    except:
        print('Invalid input, skipping', filename + '...')
        continue

    Ldf = raw_to_dataframe(datL)
    Rdf = raw_to_dataframe(datR)

    stripped_filename = os.path.split(filename)[1]
    stripped_filename = stripped_filename.split('.')[0]

    print_fig(Ldf, os.path.join('left', 'LHEMI_ALL_' + stripped_filename + '.png'))
    print_fig(Ldf, os.path.join('right', 'RHEMI_ALL_' + stripped_filename + '.png'))
    print_two_figs(Ldf, Rdf, 'BOTH_ALL_' + stripped_filename + '.png')

    curday = Ldf.iloc[0][0].date()
    endday = Ldf.iloc[-1][0].date()
    
    while curday <= endday:
        dailyLdf = Ldf.loc[(Ldf['date'] == curday)]
        dailyRdf = Rdf.loc[(Rdf['date'] == curday)]

        plt.title('Left Hemisphere ' + str(curday))
        print_fig(dailyLdf, os.path.join('left', 'LHEMI_' + str(curday) + '_' + stripped_filename + '.png'))
        plt.title('Right Hemisphere ' + str(curday))
        print_fig(dailyRdf, os.path.join('right', 'RHEMI_' + str(curday) + '_' + stripped_filename + '.png'))
        print_two_figs(dailyLdf, dailyRdf, 'BOTH_' + str(curday) + '_' + stripped_filename + '.png')

        curday += timedelta(days=1)