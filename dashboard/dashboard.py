import pymem
import pymem.process
from xml.etree import ElementTree as ET


def open_aor_process():
    pename = 'artofrally.exe'
    pm = pymem.Pymem(pename)
    return pm


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
