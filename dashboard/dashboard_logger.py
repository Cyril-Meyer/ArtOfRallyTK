import argparse
import sys
import time
from tkinter import *
import dashboard

LOG = True


def main(cheat_table_filename):
    print('ArtOfRallyTk')

    codename = str(int(time.time()))
    print(codename)
    log_filename = f'dashboard/logs/log_{codename}.csv'
    print('[INFO] ', log_filename)

    try:
        pm = dashboard.open_aor_process()
        addresses = dashboard.get_addresses(cheat_table_filename, pm)
        for k in addresses.keys():
            print('[INFO] ', k.ljust(20), hex(addresses[k][0]))
    except Exception as e:
        print('[ERROR]', e)
        exit(1)

    try:
        if LOG:
            logfile = open(log_filename, 'w')
            logfile.write('time,')
            for k in addresses.keys():
                logfile.write(k + ',')
            logfile.write('\n')
    except Exception as e:
        print('[ERROR]', e)
        exit(1)

    while True:
        try:
            if LOG:
                logfile.write(str(time.time_ns() // 1000000) + ',')
                for k in addresses.keys():
                    logfile.write(str(dashboard.get_value(addresses[k][0], addresses[k][1], pm)) + ',')
                logfile.write('\n')

            time.sleep(0.01)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('[ERROR]', e)
            continue

    if LOG:
        logfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cheattable', help='cheat table filename',
                        type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()
    main(args.cheattable)
    exit(0)
