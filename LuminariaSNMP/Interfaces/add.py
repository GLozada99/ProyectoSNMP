import sys
from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Interfaces.status import walk
from LuminariaSNMP.Racks.add import create_get_rack


try:
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        community = sys.argv[2]
        if_name_mib = 'IF-MIB::ifDescr'
        interfaces = walk(host=ip,community=community,oid=if_name_mib)
        interfaces = list(filter(None, interfaces))[1:]
        if interfaces: 
            for i,inter in enumerate(interfaces):
                try:
                    print(i,inter.split('STRING:')[-1].strip())
                except:
                    print(i,inter.split('INTEGER:')[-1].strip())

            answer = ''
            while type(answer) == str:
                answer = input('Seleccione el número de la interfaz a monitorear:').strip()
                try:
                    answer = int(answer)
                except:
                    pass
            try:
                interface = interfaces[answer].split('STRING:')[-1].strip()
            except:
                interface = interfaces[answer].split('INTEGER:')[-1].strip()
            ID, info = create_get_rack(True)
            
            if ID is None or info is None:
                raise KeyboardInterrupt

                
            db.insert_interface(ip,interface,community)
            db.resolve_rack_interface(ip,interface,ID)
        else:
            print('No se recibe respuesta SNMP, esto puede ser debido a:\nLa IP y/o el Community no son los correctos\nEl equipo no puede ser alcanzado',)
    else:
        print('Para añadir una interfaz a monitorear, ejecute el programa con los parametros: ip y community del equipo de interés.\nEj: snmpmonitor --add 10.0.0.1 public')
except KeyboardInterrupt:
    print('Proceso abortado')
finally:
    db.close()
