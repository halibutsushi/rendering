import re
from datetime import datetime
from os import listdir
from os.path import isfile, join


def get_output(path, option):
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

    print(files)


get_output(None, None)