
from LuminariaSNMP.LEDStrip.strip import LED_Strip
from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable 


db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

racks = db.get_racks()

table = BeautifulTable()
table.columns.header = ['Índice', 'Nombre']
for i,rack in enumerate(racks): 
    table.rows.append([i, rack[1]])

print(table)

answer = ''
try:
    if racks:
        while type(answer) != int:
            answer = input('Seleccione el índice del rack a probar:')
            try:
                answer = int(answer)
            except:
                pass
        if answer >= 0 and answer < len(racks):
            _,_,_,r,g,b,d = racks[answer]
            strip = LED_Strip(r,g,b,d)
            #strip.start_pwm()
            strip.change_status(0,0,0)
            while True:
                print('Escriba 1 o 0 para encender o apagar cada color respectivamente en formato [R G B]:')
                r,g,b = [int(x) for x in input().split()]
                strip.change_status(r,g,b)
        else:
            print('El rack seleccionado no existe')
            
    else:
        print('No existen racks que probar')
except KeyboardInterrupt:
    print('Prueba terminada')
finally:
    strip.off()
    db.close()

    

