from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable
from os import environ

try:
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')
    interfaces = db.get_interfaces()
    table = BeautifulTable()
    table.columns.header = ['Indice', 'IP', 'Interfaz', 'Community', 'Rack/Gabinete']
    for i,interface in enumerate(interfaces): 
        table.rows.append([i, interface[0], interface[1], interface[2], interface[3]])

    print(table)

    answer = ''
    if interfaces:
         while type(answer) != int:
            answer = input('Seleccione el índice de la interfaz a borrar:').strip()
            try:
                answer = int(answer)
            except:
                pass
    else:
        print('No existen interfaces que eliminar')
        exit(0)

    ip, interface, community, status, oid = interfaces[answer]

    db.delete_interface(ip,interface)

except KeyboardInterrupt:
    print('Proceso abortado')
finally:
    db.close()