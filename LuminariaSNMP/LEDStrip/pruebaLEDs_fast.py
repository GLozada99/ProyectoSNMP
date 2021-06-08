
from LuminariaSNMP.LEDStrip.strip import LED_Strip
from os import environ
from LuminariaSNMP.Database.DB import Database_Controler
from beautifultable import BeautifulTable 
from time import sleep

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

racks = db.get_racks()

table = BeautifulTable()
table.columns.header = ['Índice', 'Nombre']
for i,rack in enumerate(racks): 
    table.rows.append([i, rack[1]])

print(table)
states = [
    (0,0,0),(1,0,0),
    (1,1,0),(0,1,0),
    (0,1,1),(0,0,1),
    (1,0,1),(1,1,1)
]
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
            strip.change_status(0,0,0)
            while True:
                for state in states:
                    r,g,b = state
                    strip.change_status(*state)
                    sleep(0.5)

        else:
            print('El rack seleccionado no existe')
            
    else:
        print('No existen racks que probar')
except KeyboardInterrupt:
    print('Prueba terminada')
finally:
    strip.off()
    db.close()

    

