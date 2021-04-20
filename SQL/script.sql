SET autocommit = OFF;

START TRANSACTION;
DROP DATABASE IF EXISTS SNMPdata;
CREATE DATABASE SNMPdata;

USE SNMPdata;

CREATE TABLE interfaces(
    IP VARCHAR(50),
    INTERFACE VARCHAR(35),
    COMMUNITY VARCHAR(35) NOT NULL,
    ACTIVE BIT DEFAULT 1,
    CONSTRAINT PK_IP_INTERFACE PRIMARY KEY (IP, INTERFACE)
);

CREATE TABLE status_log(
    ID INTEGER AUTO_INCREMENT,
    IP VARCHAR(50) NOT NULL,
    INTERFACE VARCHAR(35) NOT NULL,
    DOWNTIME DATETIME NOT NULL,
    UPTIME DATETIME,
    CONSTRAINT PK_ID_LOG PRIMARY KEY (ID),
    CONSTRAINT UC_INT_DOWN UNIQUE (IP,INTERFACE,DOWNTIME)
);

CREATE TABLE racks(
    ID INTEGER AUTO_INCREMENT,
    INFO VARCHAR(100) NOT NULL,
    ACTIVE BIT DEFAULT 1,
    RED INTEGER,
    GREEN INTEGER,
    BLUE INTEGER,
    DOOR INTEGER,
    CONSTRAINT PK_ID_RACKS PRIMARY KEY (ID),
    CONSTRAINT UC_INFO_RACKS UNIQUE (INFO),
    CONSTRAINT R_G_diff CHECK (RED<>GREEN),
    CONSTRAINT R_B_diff CHECK (RED<>BLUE),
    CONSTRAINT B_G_diff CHECK (BLUE<>GREEN),
    CONSTRAINT D_G_diff CHECK (DOOR<>GREEN),
    CONSTRAINT D_B_diff CHECK (DOOR<>BLUE),
    CONSTRAINT D_R_diff CHECK (DOOR<>RED)
);

CREATE TABLE racks_interfaces(
    IP VARCHAR(50),
    ID_rack INTEGER,
    INTERFACE VARCHAR(35),
    CONSTRAINT PK_RACKS_INTERFACES PRIMARY KEY (IP,INTERFACE,ID_rack),
    CONSTRAINT FK_RACKS_INTERFACES_Interfaces FOREIGN KEY (IP,INTERFACE) REFERENCES interfaces(IP,INTERFACE),
    CONSTRAINT FK_RACKS_INTERFACES_Rack FOREIGN KEY (ID_rack) REFERENCES racks(ID)
);

DELIMITER |;
CREATE OR REPLACE PROCEDURE insert_interface(
    IN ipi VARCHAR(50),
    IN interfacei VARCHAR(35),
    IN communityi VARCHAR(35)
)
BEGIN
    IF EXISTS (SELECT * FROM interfaces WHERE IP=ipi AND INTERFACE=interfacei) THEN
        UPDATE interfaces SET ACTIVE=1, COMMUNITY=communityi WHERE IP = ipi AND INTERFACE = interfacei;
    ELSE
        INSERT INTO interfaces (IP,INTERFACE,COMMUNITY) VALUES (ipi, interfacei, communityi);
    END IF;
END;
|;
    
CREATE OR REPLACE PROCEDURE insert_rack(
    IN infoi VARCHAR(100),
    IN redi INTEGER,
    IN greeni INTEGER,
    IN bluei INTEGER,
    IN doori INTEGER
)
BEGIN
    IF EXISTS (SELECT * FROM racks WHERE INFO=infoi) THEN
        UPDATE racks SET ACTIVE=1, RED=redi, GREEN=greeni, BLUE=bluei, DOOR=doori WHERE INFO = infoi;
    ELSE
        INSERT INTO racks (INFO,RED,GREEN,BLUE,DOOR) VALUES (infoi, redi, greeni, bluei, doori);
    END IF;
END;
|;

CREATE OR REPLACE PROCEDURE get_interfaces_racks()
BEGIN
    SELECT i.IP, i.INTERFACE, i.COMMUNITY, r.INFO FROM interfaces AS i INNER JOIN racks_interfaces AS ri ON i.IP = ri.IP AND i.INTERFACE = ri.INTERFACE INNER JOIN racks AS r ON r.ID = ri.ID_rack WHERE i.ACTIVE = 1;
END;
|;

CREATE OR REPLACE PROCEDURE get_down_interfaces()
BEGIN
    SELECT i.IP, i.INTERFACE, r.INFO, sl.DOWNTIME FROM interfaces AS i INNER JOIN racks_interfaces AS ri ON i.IP = ri.IP AND i.INTERFACE = ri.INTERFACE INNER JOIN racks AS r ON r.ID = ri.ID_rack INNER JOIN status_log AS sl ON i.IP = sl.IP AND i.INTERFACE = sl.INTERFACE WHERE i.ACTIVE = 1 AND sl.UPTIME IS NULL;
END;
|;

CREATE OR REPLACE PROCEDURE get_log()
BEGIN
    SELECT sl.ID, sl.IP, sl.INTERFACE, sl.DOWNTIME, sl.UPTIME FROM status_log AS sl INNER JOIN interfaces AS i ON i.IP = sl.IP AND i.INTERFACE = sl.INTERFACE WHERE i.ACTIVE = 1 ORDER BY id ASC LIMIT 50;
END;
|;

CREATE OR REPLACE PROCEDURE remove_interface(
    IN ipi VARCHAR(50),
    IN interfacei VARCHAR(35)
)
BEGIN
    UPDATE interfaces SET ACTIVE=0 WHERE IP = ipi AND INTERFACE = interfacei;
    DELETE FROM racks_interfaces WHERE IP = ipi AND INTERFACE = interfacei;
END;
|;

DELIMITER |;
CREATE OR REPLACE PROCEDURE remove_rack(
    IN IDi INTEGER
)
BEGIN
    UPDATE racks SET ACTIVE = 0 WHERE ID = IDi;
    UPDATE interfaces i INNER JOIN racks_interfaces ri ON i.IP = ri.IP AND i.INTERFACE = ri.INTERFACE INNER JOIN racks r ON r.ID = ri.ID_rack SET i.ACTIVE = 0 WHERE r.ID = IDi;
END;
|;

DELIMITER |;
CREATE OR REPLACE PROCEDURE resolve_rack_interface(
    IN ipi VARCHAR(50),
    IN interfacei VARCHAR(35),
    IN id_racki INTEGER
)
BEGIN
    IF EXISTS (SELECT * FROM racks_interfaces WHERE IP = ipi AND INTERFACE = interfacei) THEN
        UPDATE racks_interfaces SET ID_rack = id_racki WHERE IP = ipi AND INTERFACE = interfacei;
    ELSE
        INSERT INTO racks_interfaces (IP,INTERFACE,ID_rack) VALUES (ipi, interfacei, id_racki);
    END IF;
END;
|;


DELIMITER ;

COMMIT;