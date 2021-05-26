from LuminariaSNMP.Database.DB import Database_Controler
from os import environ
import RPi.GPIO as GPIO

def turn_off():
    db = Database_Controler(environ.get('MARIADB_USER'),environ.get('MARIADB_PASSWORD'),'SNMPdata')

    racks = db.get_racks()
    db.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


    for rack in racks: 
        GPIO.setup(rack[3], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(rack[4], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(rack[5], GPIO.OUT, initial=GPIO.LOW)

if __name__ == '__main__':
    turn_off()

