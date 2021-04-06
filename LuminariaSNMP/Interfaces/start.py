import time
from os import environ
from itertools import chain
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Interfaces.status import get_status
from LuminariaSNMP.LEDStrip.strip import LED_Strip
from LuminariaSNMP.LEDStrip.offpins import turn_off

db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
try:
    racks = db.get_racks()

    strip_lis = dict()

    for rack in racks:
        name = rack[1]
        r = int(rack[3])
        g = int(rack[4])
        b = int(rack[5])
        strip = LED_Strip(r,g,b)
        strip.start_pwm(10000)
        strip_lis[name] = strip
        strip.white()

    time.sleep(3)
    good_racks = set()
    for rack in racks:
        name = rack[1]
        good_racks.add(name)
        strip_lis[name].off()

    interfaces = db.get_interfaces()

    down_interfaces = set([(inter[0], inter[1], inter[3]) for inter in db.get_down_interfaces()])

    while interfaces:
        for ip, interface, community, rack in interfaces:
            status = get_status(ip, interface, community)
            if not status:
                strip_lis[rack].error()
                down_interfaces.add((ip, interface, rack))
                good_racks.discard(rack)
                db.insert_down_log(ip, interface)
                print(f'Interface {interface} on host {ip} is down')
            elif (ip, interface, rack) in down_interfaces:
                down_interfaces.remove(((ip, interface, rack)))
                if rack not in chain(*down_interfaces):
                    good_racks.add(rack)
                db.insert_up_log(ip, interface)
                
        for rack in good_racks:
            strip_lis[rack].all_good()
    else:
        print('No existen interfaces a monitorear')
except KeyboardInterrupt:
    print('\nMonitoreo detenido')
finally:
    turn_off()
    db.close()
