import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import walk

logpath = 'dashboard-logger/logs/'
outpath = 'dashboard-logger/logs_view/'
logfiles = []
for (dirpath, dirnames, filenames) in walk(logpath):
    logfiles.extend(filenames)

for logfile in logfiles:
    name = logfile[4:-4]

    df = pd.read_csv(logpath + logfile).dropna(how='all', axis='columns')
    df['Acceleration'] = (df['Speed pointer 1'].diff()*10).rolling(10).sum()
    df['RPM'] = df['RPM pointer 1'].rolling(5).sum()/5
    # truncate before the start
    trunc = df[df['Gear pointer 1'] == 2].index[0] - df.index[0]
    trunc = df[df['Speed pointer 1'] >= 10].index[0] - df.index[0] - 30
    df = df.truncate(before=trunc-1)
    df = df.reset_index()
    df['Gear pointer 1'] = (df['Gear pointer 1']-1)*25

    fig = plt.figure(figsize=(12, 4))
    plt.title(name)
    plt.xlim(0, 750)
    plt.ylim(-20, 200)

    plt.axhline(y=0, color='#000000', linestyle='-')
    df['Speed pointer 1'].plot(color='#0000ff', label='Speed', legend=True)
    df['Acceleration'].plot(color='#00ffff', label='Acceleration', legend=True)
    df['RPM'].plot(color='#ff0000', label='RPM', secondary_y=True, legend=True)
    df['Gear pointer 1'].plot(color='#00ff00', label='Gear', legend=True)

    ax = fig.get_axes()
    ax[1].set_ylim(0, 10000)

    plt.savefig(outpath + name + '.png')
# plt.show()
