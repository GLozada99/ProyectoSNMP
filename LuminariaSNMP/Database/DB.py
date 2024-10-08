# Module Imports
import mariadb
from datetime import datetime
import sys

class Database_Controler():
    def __init__(self,user,password,database,host='localhost',port=3306):
        try:
            self.connection = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
            )
            self.cursor = self.connection.cursor()
            self.database = database
        except mariadb.Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            sys.exit(1)
    
    def insert_interface(self,ip,interface,community,oid_num) -> None:
        try:
            self.cursor.execute('CALL insert_interface(?, ?, ?, ?)',(ip,interface,community,oid_num))
            self.connection.commit()
        except mariadb.Error as e:
            print(f'Error al insertar interfaz: {self.database} : {e}')
            sys.exit(1)
    
    def insert_rack(self,information, R, G, B, D):
        try:
            self.cursor.execute('CALL insert_rack(?, ?, ?, ?, ?)',(information, R, G, B, D))
            self.cursor.execute('SELECT * FROM racks WHERE INFO = ?',(information,))
            ID = self.cursor.fetchall()[0][0]
            self.connection.commit()
            return ID
        except mariadb.Error as e:
            print(f'Error al insertar rack: {e}')
            sys.exit(1)
    
    def resolve_rack_interface(self,ip,interface,ID_rack):
        try:
            self.cursor.execute(
            'CALL resolve_rack_interface(?, ?, ?)',(ip,interface,ID_rack))
            self.connection.commit()
        except mariadb.Error as e:
            print(e)
            sys.exit(1)
            
    def get_interfaces(self):
        try:
            self.cursor.execute(
            'CALL get_interfaces_racks()')
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f'Error obteniendo interfaces: {e}')
            sys.exit(1)
    
    def get_racks(self):
        try:
            self.cursor.execute(
            'SELECT * FROM racks WHERE ACTIVE = 1')
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f'Error obteniendo racks: {e}')
            sys.exit(1)
    
    def delete_interface(self,ip,interface):
        try:
            self.cursor.execute(
            'CALL remove_interface(?, ?)',
            (ip,interface))
            self.connection.commit()
        except mariadb.Error as e:
            print(f'Error borrando interfaz: {e}')
            sys.exit(1)
    
    def delete_rack(self,ID):
        try:
            self.cursor.execute(
            'CALL remove_rack(?)',
            (ID,))
            self.connection.commit()
        except mariadb.Error as e:
            print(f'Error borrando rack: {e}')
            sys.exit(1)
    
    def insert_down_log(self,ip,interface):
        self.cursor.execute('SELECT * FROM status_log WHERE IP = ? AND interface=? AND UPTIME IS NULL',(ip,interface))
        if not self.cursor.fetchall():
            self.cursor.execute(
            'INSERT INTO status_log (IP,INTERFACE,DOWNTIME) VALUES (?, ?, ?)',(ip,interface,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.connection.commit()            
    
    def insert_up_log(self,ip,interface):
        self.cursor.execute(
        'UPDATE status_log SET UPTIME=? WHERE IP = ? AND interface = ? AND  UPTIME IS NULL',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ip,interface))
        self.connection.commit()

    def get_log(self,cant=100):
        try:
            self.cursor.execute('CALL get_log(?)',(cant,))
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f'Error obteniendo log: {e}')
            sys.exit(1)

    def get_down_interfaces(self):
        try:
            self.cursor.execute('CALL get_down_interfaces()')
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f'Error obteniendo log: {e}')
            sys.exit(1)
    
    def get_rack_with_info(self, info):
        try:
            self.cursor.execute('SELECT * FROM racks WHERE INFO = ?',(info))
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f'Error obteniendo racks: {e}')
            sys.exit(1)

    def close(self):
        self.connection.close()
