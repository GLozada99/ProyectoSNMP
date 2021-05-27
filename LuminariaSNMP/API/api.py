from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Interfaces.status import walk

user = environ.get('MARIADB_USER')
password = environ.get('MARIADB_PASSWORD')
database = 'SNMPdata'

def get_interfaces():
    db = Database_Controler(user,password,database)
    interfaces = db.get_interfaces()
    db.close()
    return interfaces

def remove_interface(ip,interface):
    db = Database_Controler(user,password,database)
    db.delete_interface(ip,interface)
    db.close()

def insert_interface(ip,interface,community,oid_num):
    db = Database_Controler(user,password,database)
    db.insert_interface(ip,interface,community,oid_num)
    db.close()

def get_snmp_interfaces(ip,community):
    raw_interfaces = walk(host=ip,community=community,oid='ifDescr')
    interfaces = list(filter(None, raw_interfaces))[1:]
    return interfaces

def insert_rack_get_id(info, R, G, B, D):
    db = Database_Controler(user,password,database)
    ID = db.insert_rack(info, R, G, B, D)
    db.close()
    return ID

def insert_interface_new_rack(ip,interface,community,oid_num,info, R, G, B, D):
    insert_interface(ip,interface,community,oid_num)
    ID = insert_rack_get_id(info, R, G, B, D)
    db = Database_Controler(user,password,database)
    db.resolve_rack_interface(ip,interface, ID)
    db.close()

def get_log(cant=100):
    
    

