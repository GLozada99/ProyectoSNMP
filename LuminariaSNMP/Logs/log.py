from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')

log = db.get_log()
db.close()
table = BeautifulTable()
table.columns.header = ['IP', 'Interfaz', 'Hora de caída', 'Hora de subida', 'Tiempo caído']
for entry in log:
    subida = entry[4]
    try:
        total = entry[4] - entry[3]
    except TypeError:
        total = 'N/A'
        subida = 'Continúa caído'
    table.rows.append([entry[1], entry[2], str(entry[3]), str(subida), total])

print(table)
