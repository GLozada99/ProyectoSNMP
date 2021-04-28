from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

log = db.get_down_interfaces()
db.close()
table = BeautifulTable()
table.columns.header = ['IP', 'Interfaz', 'Rack/Gabinete', 'Hora de caída']
if log:
    for entry in log: 
        table.rows.append([entry[0], entry[1], entry[2], str(entry[3])])
else:
    print('No hay interfaces caídas')
print(table)