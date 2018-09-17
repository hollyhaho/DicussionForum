CREATE TABLE  IF NOT EXISTS user(
	Id INTEGER PRIMARY KEY ASC, 
	username TEXT, 
	password TEXT
);

CREATE TABLE IF NOT EXISTS forums(
	id INTEGER PRIMARY KEY ASC, 
	forum_name TEXT, 
	forum_creator INTEGER,
	forum_time DATETIME,
	FOREIGN KEY (forum_creator) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS threads(
	thread_id INTEGER PRIMARY KEY ASC,
	thread_title TEXT NOT NULL,
	thread_creator INTEGER NOT NULL,
	thread_time TEXT,
	forum_id INTEGER,
	FOREIGN KEY (forum_id) REFERENCES forums(id),
	FOREIGN KEY (thread_creator) REFERENCES user(id)
);



INSERT INTO USER VALUES (1, "hoangphuc", "love" );
INSERT INTO FORUMS VALUES (1, "Testing", 1, "2017-09-16 15:33:33.12343" );
INSERT INTO THREADS VALUES (1,"Whydo?", 1, "2017-09-14 15:33:33.123433",1);
INSERT INTO USER VALUES (2, "holly", "ha" );
INSERT INTO FORUMS VALUES (2, "Testing222", 2, "2017-09-16 15:33:33.12343" );
INSERT INTO THREADS VALUES (2,"Whydo22?", 2, "2017-09-14 15:33:33.123433",2);