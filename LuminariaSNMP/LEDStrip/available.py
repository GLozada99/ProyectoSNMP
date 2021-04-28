from LuminariaSNMP.Database.DB import Database_Controler
from os import environ
from beautifultable import BeautifulTable 

def get_available_pins(extra=set()):
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

    racks = db.get_racks()
    db.close()

    table = BeautifulTable()
    table.columns.header = ['Pins']
    available_pins = {3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40} | extra
    for rack in racks: 
        available_pins.difference_update([rack[3], rack[4], rack[5], rack[6]])

    available_pins |=  extra    
    for pin in available_pins:
        table.rows.append([pin,])

    
    
    return (available_pins, table)

if __name__ == '__main__':
    print(get_available_pins()[1])