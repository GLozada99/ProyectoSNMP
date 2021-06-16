from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Interfaces.status import walk

_user = environ.get('MARIADB_USER')
_password = environ.get('MARIADB_PASSWORD')
_database = 'SNMPdata'

def insert_interface(ip,interface,community,oid_num):
    db = Database_Controler(_user,_password,_database)
    db.insert_interface(ip,interface,community,oid_num)
    db.close()

def insert_rack_get_id(info, R, G, B, D):
    db = Database_Controler(_user,_password,_database)
    ID = db.insert_rack(info, R, G, B, D)
    db.close()
    return ID

def resolve_interface_rack(ip,interface,ID):
    db = Database_Controler(_user,_password,_database)
    db.resolve_rack_interface(ip,interface, ID)
    db.close()

def get_snmp_interfaces(ip,community):
    raw_interfaces = walk(host=ip,community=community,oid='ifDescr')
    interfaces = list(filter(None, raw_interfaces))[1:]
    return interfaces

def get_interfaces():
    db = Database_Controler(_user,_password,_database)
    interfaces = db.get_interfaces()
    db.close()
    return interfaces

def get_racks():
    db = Database_Controler(_user,_password,_database)
    interfaces = db.get_racks()
    db.close()
    return interfaces

def get_down_interfaces():
    db = Database_Controler(_user,_password,_database)
    interfaces = db.get_down_interfaces()
    db.close()
    return interfaces

def get_log(cant=100):
    db = Database_Controler(_user,_password,_database)
    log = db.get_log(cant)
    db.close()
    return log
    
def remove_interface(ip,interface):
    db = Database_Controler(_user,_password,_database)
    db.delete_interface(ip,interface)
    db.close()


    

