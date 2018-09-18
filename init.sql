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



insert into threads (thread_title, thread_creator, forum_id) values ('Does anyone know how to start Redis?', 'bob', 1);

insert into threads (thread_title, thread_creator, forum_id) values ('Has anyone heard of Edis?', 'charlie', 1);

insert into forums (forum_name, forum_creator) values ('redis', 'alice');

insert into forums (forum_name, forum_creator) values ('mongodb', 'bob');
