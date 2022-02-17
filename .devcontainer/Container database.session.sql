DROP TABLE IF EXISTS user_info;
DROP TABLE IF EXISTS weather_info;

CREATE TABLE IF NOT EXISTS user_info (
	user_id uuid PRIMARY KEY,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	role TEXT NOT NULL DEFAULT 'USER'
);

CREATE TABLE IF NOT EXISTS weather_info (
	record_id SERIAL PRIMARY KEY,
	location TEXT NOT NULL,
	condition TEXT NOT NULL,
	temperature FLOAT NOT NULL,
    time TIMESTAMP NOT NULL
);

INSERT INTO user_info(user_id, username, password, role)
VALUES 
	('5665a0a4-2fc6-4598-9d8e-1af0f13c087f', 'user_1', 'user_1', 'USER'),
 	('d6c9e63d-2a58-457d-b8a5-ee26fbe9458a', 'admin_1', 'admin_1', 'ADMIN');

INSERT INTO weather_info(time, location, condition, temperature)
VALUES 
	('2022-02-11 13:10:25-07', 'Pendik', 'Sunny', 8),
	('2022-02-13 13:10:25-07', 'Pendik', 'Sunny',8),
	('2022-02-13 13:10:25-08', 'Tuzla', 'Rain',5),
	('2022-02-13 13:10:25-09', 'Kartal', 'Sunny',9),
	('2022-02-14 13:10:25-09', 'Pendik', 'Rain',4),
	('2022-02-14 13:10:25-10', 'Tuzla', 'Snow',0),
	('2022-02-14 13:10:25-11', 'Kartal', 'Rain',4),
	('2022-02-15 13:10:25-09', 'Pendik', 'Sunny',10),
	('2022-02-15 13:10:25-10', 'Tuzla', 'Rain',6),
	('2022-02-15 13:10:25-11', 'Kartal', 'Sunny',11);

SELECT * FROM user_info;
SELECT * FROM weather_info;