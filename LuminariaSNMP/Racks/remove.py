from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable 

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')

racks = db.get_racks()

table = BeautifulTable()
table.columns.header = ['Índice', 'Nombre']
for i,rack in enumerate(racks): 
    table.rows.append([i, rack[1]])

print(table)

answer = ''
try:
    if racks:
        while type(answer) == str:
            answer = input('Seleccione el índice del rack a borrar (recuerde que esto borrará todas las interfaces en el rack):')
            try:
                answer = int(answer)
            except:
                pass
        if answer >= 0:
            db.delete_rack(racks[answer][0])
            
    else:
        print('No existen racks que eliminar')
except KeyboardInterrupt:
    pass
finally:
    db.close()

#print(f'La interfaz es {interface}')
