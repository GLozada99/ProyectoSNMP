from os import environ
from beautifultable import BeautifulTable 
from LuminariaSNMP.Database.DB import Database_Controler

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

racks = db.get_racks()
db.close()

table = BeautifulTable()
table.columns.header = ['ID', 'Nombre', 'R', 'G', 'B', 'D']
for rack in racks: 
    table.rows.append([rack[0], rack[1], rack[3], rack[4], rack[5], rack[6]])

print(table)