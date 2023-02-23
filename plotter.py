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

