import sys
import time
from tkinter import *
import pymem
import pymem.process
from xml.etree import ElementTree as ET

LOG = True


def get_runtime_address(module, address, offsets, pm):
    read_address = pm.read_longlong
    x = pymem.process.module_from_name(pm.process_handle, module).lpBaseOfDll
    x = read_address(x + address)
    for offset in offsets[::-1][0:-1]:
        x = read_address(x + offset)
    return x + offsets[0]


def get_value(address, variable_type, pm):
    if variable_type == 'Float':
        return pm.read_float(address)
    elif variable_type == '4 Bytes':
        return pm.read_long(address)
    else:
        raise NotImplementedError
    return


def get_addresses(filename, pm):
    addresses = {}
    for entry in ET.parse(filename).getroot().find('CheatEntries').findall('CheatEntry'):
        if '1' in entry.find('Description').text:
            description = entry.find('Description').text[1:-1]
            module, address = entry.find('Address').text.split('+')
            variable_type = entry.find('VariableType').text
            offsets = []
            for offset in entry.find('Offsets').findall('Offset'):
                offsets.append(int(offset.text, 16))
            address = get_runtime_address(module[1:-1], int(address, 16), offsets, pm)
            addresses[description] = (address, variable_type)
    return addresses


def main():
    print('ArtOfRallyTk')

    codename = str(int(time.time()))
    if len(sys.argv) > 1:
        codename = sys.argv[1]
    log_filename = f'dashboard/logs/log_{codename}.csv'
    print('[INFO] ', log_filename)

    try:
        pename = 'artofrally.exe'
        pm = pymem.Pymem(pename)
        addresses = get_addresses('cheat-table/artofrally.CT', pm)
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
                    logfile.write(str(get_value(addresses[k][0], addresses[k][1], pm)) + ',')
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
    main()
    exit(0)
