from os import environ
from LuminariaSNMP.Database.DB import Database_Controler

def create_get_rack(choose):
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
    if choose:
        racks = db.get_racks()

        for i,rack in enumerate(racks):
            print(i,rack[1])
        
        answer = ''
        response = ''  
        while type(answer) == str:
            if racks:
                answer = input('Seleccione el número del rack en el que se encuentra el equipo. Si desea agregar un rack, ingrese "-1".')
                response = 'Y' if answer == '-1' else 'n'
            else:
                answer = -1
                response = input('No existen Racks. ¿Desea agregar uno? [Y/n]')
            try:
                answer = int(answer)
            except:
                pass
    else:
        answer = -1
        response = 'Y'
    
    if answer >= 0:
        ID = racks[answer][0]
        info = racks[answer][1]
    elif answer == -1:
        if response.upper() == 'Y':
            info = input('Introduzca el nombre/información del rack a agregar:').strip()
            R, G, B = [int(x) for x in input('Introduzca pines a controlar los colores en formato [R G B]:').strip().split()]
            ID = db.insert_rack(info, R, G, B)
        else:
            exit(0)
    
    return((ID,info))

if __name__ == '__main__':
    create_get_rack(False)