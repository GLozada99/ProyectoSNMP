from os import environ
from beautifultable import BeautifulTable 
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Racks.add import create_get_rack


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
            answer = input('Seleccione el índice del rack a editar:')
            try:
                answer = int(answer)
            except:
                pass
        if answer >= 0:
            try:
                rack = racks[answer]
            except IndexError:
                print('Debe seleccionar uno de los racks listados')
                raise KeyboardInterrupt
            table = BeautifulTable()
            table.columns.header = ['ID', 'Nombre', 'R', 'G', 'B', 'D']
            table.rows.append([rack[0], rack[1], rack[3], rack[4], rack[5], rack[6]])
            print('Estos son los datos actuales:')
            print(table)
            create_get_rack(False,rack) 
            #db.delete_rack(racks[answer][0])
            
    else:
        print('No existen racks')
except KeyboardInterrupt:
    pass
finally:
    db.close()

#print(f'La interfaz es {interface}')
