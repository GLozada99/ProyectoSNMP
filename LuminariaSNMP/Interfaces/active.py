from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
interfaces = db.get_interfaces()
db.close()

table = BeautifulTable()
table.columns.header = ['IP', 'Interfaz', 'Community', 'Rack/Gabinete']
for interface in interfaces: 
    table.rows.append([interface[0],interface[1],interface[2],interface[3]])

print(table)