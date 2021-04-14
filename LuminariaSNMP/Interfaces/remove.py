from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable
from os import environ

try:
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')

    interfaces = db.get_interfaces()


    table = BeautifulTable()
    table.columns.header = ["Indice", "IP", "Interfaz", "Community", "Rack/Gabinete"]
    for i,interface in enumerate(interfaces): 
        table.rows.append([i, interface[0], interface[1], interface[2], interface[3]])

    print(table)

    answer = ''
    if interfaces:
        while type(answer) == str:
            answer = input('Seleccione el índice de la interfaz a borrar:').strip()
            try:
                answer = int(answer)
            except:
                pass
    else:
        print('No existen interfaces que eliminar')
        exit(0)

    ip, interface, community, status = interfaces[answer]

    db.delete_interface(ip,interface)

except KeyboardInterrupt:
    print('Proceso abortado')
finally:
    db.close()