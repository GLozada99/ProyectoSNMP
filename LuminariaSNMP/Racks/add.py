from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.LEDStrip.available import get_available_pins
def create_get_rack(choose: bool):
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
    try:
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
        
        print(answer)
        if answer >= 0:
            ID = racks[answer][0]
            info = racks[answer][1]
            print(ID,info)
        elif answer == -1:
            if response.upper() == 'Y':
                info = input('Introduzca el nombre/información del rack a agregar:').strip()
                info_pins = get_available_pins()

                print(info_pins[1])
                R, G, B = [int(x) for x in input('Esos son los pines disponibles. Introduzca pines a controlar los colores en formato [R G B]:').strip().split()]
                D = int(input('Introuzca el pin destinado al monitoreo de la puerta:').strip())

                
                chosen_pins = [R, G, B, D]
                if len(set(chosen_pins)) == 4:
                    bad_pins = [x for x in chosen_pins if x not in info_pins[0]]
                    if not bad_pins:
                        ID = db.insert_rack(info, R, G, B, D)
                    else:
                        raise Exception
                else:
                    bad_pins = None
                    raise Exception
                    
            else:
                ID = None
                info = None
    except KeyboardInterrupt:
        ID = None
        info = None
        print('Proceso abortado')
    except Exception:
        print('No es posible insertar rack.')
        if bad_pins:
            print('Los pines siguientes no se encuentran disponibles:', *bad_pins)
        else:
            print('Existe uno o más pines repetidos:',*chosen_pins)
        
        ID = None
        info = None
    except ValueError as e:
        ID = None
        info = None
        print(e)
    finally:
        
        db.close()
        return((ID,info))

if __name__ == '__main__':
    create_get_rack(False)