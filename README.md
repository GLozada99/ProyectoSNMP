Todos los comandos serán introducidos desde el directorio raiz del proyecto.

Instalar todo lo necesario:

    sudo source instalation
Acceder a mariadb: 

    sudo mysql -u root
Crear usuario de MariaDB:
    
    CREATE USER IF NOT EXISTS '<USUARIO>'@'localhost';
    SET PASSWORD FOR '<USUARIO>'@'localhost' = PASSWORD('<CONTRASEÑA>');
Dar privilegios al usuario:

    GRANT ALL PRIVILEGES ON *.* TO '<USUARIO>'@'localhost' IDENTIFIED BY '<CONTRASEÑA>';
    FLUSH PRIVILEGES;
Salir de mariadb:

    exit
Definir variable de ambiente para usuario y contraseña de mariadb:

    printf $"\nexport MARIADB_USER=<USUARIO>\n" >> ~/.profile
    printf $"\nexport MARIADB_PASSWORD=<CONTRASEÑA>\n" >> ~/.profile
Usando:

    cat ~/.profile
Confirmar que en el archivo ~/.profile deben encontrarse las siguientes lineas:
    
    export PATH=Distintas/Rutas:Ruta/a/Bash
    export MARIADB_USER=<USUARIO>
    export MARIADB_PASSWORD=<CONTRASEÑA>
Si es correcto lo anterior, registrar cambios con:
    
    source ~/.bash_profile
Generar base de datos:

    sudo mysql -h localhost -u root < SQL/script.sql
Configurar agente SNMP:
    
    sudo nano /etc/snmp/snmpd.conf
    Agregar la linea: rocommunity public
    Agregar la línea: agentAddress udp:161
    Comentar la línea: agentAddress udp:127.0.0.1:161
Ingresar a cron:

    crontab -e
Agregar a cron la siguiente línea:

    SHELL=/bin/bash
    MARIADB_USER=<USUARIO>
    MARIADB_PASSWORD=<CONTRASEÑA>
    @reboot sleep 6 && PYTHONPATH=ruta/abs/dir/raiz/proyecto/ ruta/abs/dir/raiz/proyecto/Bash/snmpmonitor --start
Finalizar instalación

    .Help/finalize


Para utilizar la herramienta, se utiliza el comando:
    
    snmpmonitor
Usándolo con --help provee información de todas sus opciones:
    
    snmpmonitor --help

Al agregar un rack, se utilizan los números de los pines que indican los colores de la cinta LED RGB. Para saber cuales pines usar, se tiene el pinout de la Raspberry Pi 4


![Raspberry Pi 4 Pinout](https://github.com/GLozada99/ProyectoSNMP/blob/master/RPi4-Pinout.jpg)

Los números a utilizar son los más cercanos al centro. Es decir, el que está descrito como GPIO 0 será designado como 11 en la aplicación, y el GPIO 4 será el 16.
