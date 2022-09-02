-- DROP DATABASE db_lidar_air;
-- CREATE DATABASE db_lidar_air;

DROP TABLE IF EXISTS LIDAR;
DROP TABLE IF EXISTS AIR;
DROP TABLE IF EXISTS DEVICE;
DROP TABLE IF EXISTS DEVICETYPE;

CREATE TABLE DEVICETYPE(
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE DEVICE(
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    type_id INT NOT NULL DEFAULT 1,
    FOREIGN KEY (type_id) REFERENCES DEVICETYPE(id)
);

CREATE TABLE LIDAR(
    id INT PRIMARY KEY AUTO_INCREMENT,
    people INT NOT NULL DEFAULT -1,
    vehicles INT NOT NULL DEFAULT -1,
    device_id INT NOT NULL,
    timedate DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (device_id) REFERENCES DEVICE(id)
);

CREATE TABLE AIR(
    id INT PRIMARY KEY AUTO_INCREMENT,
    aqi INT NOT NULL,
    so2 INT NOT NULL,
    no2 INT NOT NULL,
    o3 INT NOT NULL,
    pm1p0 INT NOT NULL,
    pm2p5 INT NOT NULL,
    pm10 INT NOT NULL,
    co INT NOT NULL,
    temp INT NOT NULL,
    pres INT NOT NULL,
    relhum INT NOT NULL,
    noise INT NOT NULL,
    device_id INT NOT NULL,
    timedate DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (device_id) REFERENCES DEVICE(id)
);


INSERT INTO DEVICETYPE(
	name
)VALUES(
	'default'
);

INSERT INTO DEVICE(
    name,
    type_id
)VALUES(
    'Raspberry 1',
    (SELECT dt.id
    FROM DEVICETYPE as dt
    WHERE dt.name = 'default')
);

DROP PROCEDURE IF EXISTS GenerateLidarData;
DELIMITER //
CREATE PROCEDURE GenerateLidarData(IN device_name VARCHAR(30), IN count INT)
BEGIN
    SET @ii = 1;
    SET @difference = CEIL(RAND()*59);
    SET @starting_date = (SELECT (DATE_SUB(NOW(), INTERVAL 10 DAY)));
    repetition: LOOP
        IF @ii > count THEN
            LEAVE repetition;
        END IF;

        INSERT INTO LIDAR(
            people,
            vehicles,
            timedate,
            device_id
        )VALUES(
            FLOOR(RAND()*13),
            FLOOR(RAND()*8),
            @starting_date,
            (SELECT d.id
            FROM DEVICE as d
            WHERE d.name = device_name)
        );
        SET @difference = CEIL(RAND()*59);
        SET @starting_date = (SELECT(DATE_ADD(@starting_date, INTERVAL @difference MINUTE)));
        SET @ii = @ii + 1;
        ITERATE repetition;
    END LOOP;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS GenerateAirData;
DELIMITER //
CREATE PROCEDURE GenerateAirData(IN device_name VARCHAR(30), IN count INT)
BEGIN
    SET @ii = 1;
    SET @difference = CEIL(RAND()*59);
    SET @starting_date = (SELECT (DATE_SUB(NOW(), INTERVAL 10 DAY)));
    repetition: LOOP
        IF @ii > count THEN
            LEAVE repetition;
        END IF;

        INSERT INTO AIR(
            aqi,
            so2,
            no2,
            o3,
            pm1p0,
            pm2p5,
            pm10,
            co,
            temp,
            pres,
            relhum,
            noise,
            timedate,
            device_id
        )VALUES(
            FLOOR(RAND()*30),
            FLOOR(RAND()*2),
            FLOOR(RAND()*2),
            FLOOR(RAND()*11),
            FLOOR(RAND()*11),
            FLOOR(RAND()*11),
            FLOOR(RAND()*11),
            FLOOR(RAND()*2),
            FLOOR(RAND()*90),
            FLOOR(RAND()*1500),
            FLOOR(RAND()*100),
            FLOOR(RAND()*100),
            @starting_date,
            (SELECT d.id
            FROM DEVICE as d
            WHERE d.name = device_name)
        );
        SET @difference = CEIL(RAND()*59);
        SET @starting_date = (SELECT(DATE_ADD(@starting_date, INTERVAL @difference MINUTE)));
        SET @ii = @ii + 1;
        ITERATE repetition;
    END LOOP;
END//
DELIMITER ;

CALL GenerateLidarData('Raspberry 1', 100);
CALL GenerateAirData('Raspberry 1', 100);