import sys
import subprocess

def walk(host,community='public',oid='', version='2c'):
    data = []
    process = subprocess.Popen(f'snmpwalk -Os -c {community} -v {version} {host} -Ci {oid} -t 0.1'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    while True:
        output = process.stdout.readline()
        data.append(output.strip())
        return_code = process.poll()
        if return_code is not None:
            for output in process.stdout.readlines():
                data.append(output.strip())
            return data
            break

def index_by_interface(data: list, name: str) -> str:
    for dat in data:
        try:
            oid, if_name = dat.split('=')
            if_name = if_name.split('STRING:')[-1].strip()
            if if_name.strip() == name.strip():
                number = oid.split('.')[-1]
                return number
        except: 
            pass  

def status_by_index(data: list, number: str) -> str:
    for dat in data:
        try:
            oid, status = dat.split('=')
            num = oid.split('.')[-1]
            if num.strip() == number.strip():
                status = status.split('(')[0].split()[-1]
                return status
        except:
            pass

def get_status(ip: str, comm: str, oid_num: str) -> bool:
    if_status_mib = 'ifOperStatus'
    ip = ip.strip()
    comm = comm.strip()
    oid_num = oid_num.strip()
    
    status_data = walk(ip,comm,if_status_mib)
    status = status_by_index(status_data,oid_num)
    
    result = False
    if status != None:
        result = True if status.strip() == 'up' else False
    return result
