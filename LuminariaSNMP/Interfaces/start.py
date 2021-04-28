import time
import sys
import mariadb
from os import environ
from itertools import chain
from LuminariaSNMP.Daemon.daemon import Daemon
from LuminariaSNMP.Database.DB import Database_Controler
from LuminariaSNMP.Interfaces.status import get_status
from LuminariaSNMP.LEDStrip.strip import LED_Strip
from LuminariaSNMP.LEDStrip.offpins import turn_off
class Monitor(Daemon):
    def run(self):
        db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
        try:    
            racks = db.get_racks()

            strip_lis = dict()

            for rack in racks:
                name = rack[1]
                r = int(rack[3])
                g = int(rack[4])
                b = int(rack[5])
                d = int(rack[6])
                strip = LED_Strip(r,g,b,d)
                strip.start_pwm()
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
                for ip, interface, community, rack, oid_num in interfaces:
                    status = get_status(ip, community, oid_num)
                    try:
                        if not status:
                            strip_lis[rack].error()
                            down_interfaces.add((ip, interface, rack))
                            good_racks.discard(rack)
                            insert_up_down = False
                            db.insert_down_log(ip, interface)
                            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            print(f'Interface {interface} on host {ip} is down at {current_time}')
                        elif (ip, interface, rack) in down_interfaces:
                            down_interfaces.remove(((ip, interface, rack)))
                            if rack not in chain(*down_interfaces):
                                good_racks.add(rack)
                            insert_up_down = True
                            db.insert_up_log(ip, interface)
                    except mariadb.Error as e:
                        print(f'Error insertando log a la base de datos: {e}','\n Se realizó una nueva conexión')
                        db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'127.0.0.1',3306,'SNMPdata')
                        if insert_up_down:
                            db.insert_up_log(ip, interface)
                        else:
                            db.insert_down_log(ip, interface)
                        
                for rack in good_racks:
                    strip_lis[rack].all_good()
            else:
                print('No existen interfaces a monitorear')
        except KeyboardInterrupt:
            print('\nMonitoreo detenido')
        finally:
            turn_off()
            db.close()

if __name__ == '__main__':
    monitor = Monitor('/tmp/monitor.pid',stdout='/tmp/snmpmonitor_log')
    if sys.argv[1] == 'start':
            monitor.start()
    elif sys.argv[1] == 'stop':
            monitor.stop()
    elif sys.argv[1] == 'restart':
            monitor.restart()
    elif sys.argv[1] == 'debug':
            monitor.run()
    elif sys.argv[1] == 'running':
            monitor.is_running()
    else:
        print('No se escogió una opción adecuada')
