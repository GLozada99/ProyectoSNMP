import sys
import subprocess

def walk(host, version='2c',community='public',oid=''):
    data = []
    process = subprocess.Popen(['snmpwalk','-Os','-c',community,'-v',version,host,'-Ci',oid], stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    while True:
        output = process.stdout.readline()
        data.append(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                data.append(output.strip())
            return data
            break

def index_by_interface(data,name):
    for dat in data:
        try:
            oid, if_name = dat.split('=')
            if_name = if_name.split()[-1]
            if if_name.strip() == name.strip():
                number = oid.split('.')[-1]
                return number
        except:
            pass  

def status_by_index(data,number):
    for dat in data:
        try:
            oid, status = dat.split('=')
            num = oid.split('.')[-1]
            if num.strip() == number.strip():
                status = status.split('(')[0].split()[-1]
                return status
        except:
            pass

def get_status(ip,interface,comm):
    if_name_mib = 'IF-MIB::ifName'
    if_status_mib = 'IF-MIB::ifOperStatus'
    ip = ip.strip()
    interface = interface.strip()
    comm = comm.strip()
    
    name_data = walk(ip,oid=if_name_mib,community=comm)
    status_data = walk(ip,oid=if_status_mib,community=comm)
    
    index = index_by_interface(name_data,interface)
    status = status_by_index(status_data,index)
    
    result = False
    if status != None:
        result = True if status.strip() == 'up' else False
    
    return result
