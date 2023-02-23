import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def str_to_datetime(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')

