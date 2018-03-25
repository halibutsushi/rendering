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

    files = []
    for f in file_names:
        try:
            datetime.strptime(f[8:-4], '%Y-%m-%d')
        except Exception:
            continue

        files.append(join(path, f))

    max_ram = 0
    max_cpu = 0
    sum_df = None

    get_sum = True
    if 'summary' in options:
        get_max_ram = True
        get_max_cpu = True
    else:
        get_max_ram = 'maxram' in options
        get_max_cpu = 'maxcpu' in options
        if get_max_ram or get_max_cpu:
            get_sum = False

    for f in files:
        df = pd.read_csv(f, header=None,
                         names=['id', 'app', 'renderer', 'frames', 'status', 'render_time', 'ram_usage', 'cpu_ptg'])

        if 'failed' not in options:
            df = df[df['status'] == True]

        if 'app' in options:
            df = df[df['app'] == options['app']]

        if 'renderer' in options:
            df = df[df['renderer'] == options['renderer']]

        df.fillna(0, inplace=True)

        if get_sum:
            df['count'] = 1
            new_sum = df.agg({'render_time':'sum', 'ram_usage':'sum', 'cpu_ptg':'sum', 'count':'sum'})
            if sum_df is None:
                sum_df = new_sum
            else:
                sum_df += new_sum

        if get_max_ram:
            new_ram = df['ram_usage'].max()
            if new_ram > max_ram:
                max_ram = new_ram
        if get_max_cpu:
            new_cpu = df['cpu_ptg'].max()
            if new_cpu > max_cpu:
                max_cpu = new_cpu

    if sum_df is not None:
        if sum_df['count'] > 0:
            avg_df = sum_df / sum_df['count']
        else:
            avg_df = sum_df

    if get_sum and get_max_cpu:
        print(avg_df['render_time'])
        print(avg_df['cpu_ptg'])
        print(avg_df['ram_usage'])
        print(max_ram)
        print(max_cpu)
    elif get_max_cpu:
        print(max_cpu)
    elif get_max_ram:
        print(max_ram)
    elif 'avgtime' in options:
        print(avg_df['render_time'])
    elif 'avgcpu' in options:
        print(avg_df['cpu_ptg'])
    elif 'avgram' in options:
        print(avg_df['ram_usage'])
    else:
        print(sum_df['count'])

get_output(None, {'avgtime':None})
#get_output(None, {'failed':None, 'avgtime':None})
#get_output(None, {'app':'app2', 'summary':None})
#get_output(None, {'renderer':'Xiao Lee', })