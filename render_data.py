#!/usr/bin/env python

import argparse
import re
from datetime import datetime
from os import listdir, getcwd
from os.path import isfile, join

import pandas as pd


def get_output(args):
    path = args.path
    # regular expression for rendering files
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
    # if there is -summary flag, calculate all max values and sum values
    if args.summary:
        get_max_ram = True
        get_max_cpu = True
    else:
        get_max_ram = args.maxram
        get_max_cpu = args.maxcpu
        # if there is no -summary flag and there is either one of max value flags do not calculate sum values
        if get_max_ram or get_max_cpu:
            get_sum = False

    # for each files calculate sum values and max values according to the input flags
    for f in files:
        df = pd.read_csv(f, header=None,
                         names=['id', 'app', 'renderer', 'frames', 'status', 'render_time', 'ram_usage', 'cpu_ptg'])

        if len(df) == 0:
            continue

        # filter rows according to the filtering flags
        if args.failed is False or args.maxram or args.maxcpu or args.summary or args.avgcpu or args.avgram \
                or args.avgtime:
            df = df[df['status'] == True]

        if args.app:
            df = df[df['app'] == args.app]

        if args.renderer:
            df = df[df['renderer'] == args.renderer]

        # filtering finished

        # set null values to zeros
        df.fillna(0, inplace=True)

        # calculate sum values, if any of average value calculation is needed
        if get_sum:
            df['count'] = 1
            new_sum = df.agg({'render_time':'sum', 'ram_usage':'sum', 'cpu_ptg':'sum', 'count':'sum'})
            if sum_df is None:
                sum_df = new_sum
            else:
                sum_df += new_sum

        # update max values
        if get_max_ram:
            new_ram = df['ram_usage'].max()
            if new_ram > max_ram:
                max_ram = new_ram
        if get_max_cpu:
            new_cpu = df['cpu_ptg'].max()
            if new_cpu > max_cpu:
                max_cpu = new_cpu

    # calculate average values
    if sum_df is not None:
        count = sum_df['count']
        if count > 0:
            avg_df = sum_df / sum_df['count']
        else:
            avg_df = sum_df

    else:
        count = 0
        avg_df = {'render_time': 0, 'cpu_ptg':0, 'ram_usage': 0}

    # print outputs
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
    elif args.avgtime:
        print(avg_df['render_time'])
    elif args.avgcpu:
        print(avg_df['cpu_ptg'])
    elif args.avgram:
        print(avg_df['ram_usage'])
    else:
        print(sum_df['count'])

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default=getcwd())
parser.add_argument('-failed', action='store_true')
parser.add_argument('-app', type=str)
parser.add_argument('-renderer', type=str)

# mutually exclusive flag group
group = parser.add_mutually_exclusive_group()
group.add_argument('-avgtime', action='store_true')
group.add_argument('-avgcpu', action='store_true')
group.add_argument('-avgram', action='store_true')
group.add_argument('-maxram', action='store_true')
group.add_argument('-maxcpu', action='store_true')
group.add_argument('-summary', action='store_true')
args = parser.parse_args()

# print(args.path)
# print(args.failed)
# print(args.app)
# print(args.renderer)
# print(args.avgtime)
# print(args.summary)

get_output(args)