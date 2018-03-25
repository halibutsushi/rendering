import re
from datetime import datetime
from os import listdir
from os.path import isfile, join

import pandas as pd


def get_output(path, options):
    if path is None:
        path = './'

    redering_file_pattern = r'renders_[0-9]{4}-[0-1][0-9]-[0-3][0-9]\.csv'
    file_names = [f for f in listdir(path) if isfile(join(path, f)) and re.match(redering_file_pattern, f)]

    print(file_names)
    files = []
    for f in file_names:
        try:
            print(f[8:-4])
            datetime.strptime(f[8:-4], '%Y-%m-%d')
        except Exception:
            continue

        files.append(join(path, f))

    for f in files:
        df = pd.read_csv(f, header=None,
                         names=['id', 'app', 'renderer', 'frames', 'status', 'render_time', 'ram_usage', 'cpu_ptg'])

        if 'failed' not in options:
            df = df[df['status'] == True]
        print(df.head())
        break


get_output(None, {})