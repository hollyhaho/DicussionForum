# webapp-discussionforum

Use Flask to create a Web Service API for a discussion forum application.

To run program, make sure you install flask and BasicAuth:
```
pip3 install flask
pip3 install Flask-BasicAuth
```
To initialize the database doing the following:
```
export FLASK_APP=auth
flask init_db
```


# API Calls

### 1. GET /forums
Curl call:
```
curl localhost:5000/forums
```
Response: Success 200 OK
```
[
	
	{
		"Id": 1,
		"forum_creator": "alice",
		"forum_name": "redis"
	},
	{
		"Id": 2,
		"forum_creator": "bob",
		"forum_name": "mongodb"
	},
	{
		"Id": 3,
		"forum_creator": "bob",
		"forum_name": "python"
	},
	{
		"Id": 4,
		"forum_creator": "bob",
		"forum_name": "flask"
	}
]
Error: If there are forums with dupl
```
### 2. POST /forums
Curl call: 
```curl -v -u holly:password -d '{"forum_name":"HTML"}' -H "Content-Type: application/json" -X POST localhost:5000/forums```

Response
Error: 409 for duplicate forum names
Success: 201 forum created

### 3.  GET /forums/<forum_id>
Curl call: 
```curl localhost:5000/forums/1```
+ Response: Success 200 OK
+ Curl call: 
```
[
	{   "Id": 1,
	    "forum_Id": 1,    "thread_creator": "bob",
	    "thread_time": "2018-09-26 04:27:21",
	    "thread_title": "Does anyone know how to start Redis?"  
	},
	{
	    "Id": 2,    "forum_Id": 1,
	    "thread_creator": "charlie",
	    "thread_time": "2018-09-26 04:27:21",    
	    "thread_title": "Has anyone heard of Edis?"
	}
]
```
### 4.  POST /forums/<forum_id>
Curl call: 
```curl -v -u holly:password -d '{"thread_title":"Love", "text": "I love you"}' -H "Content-Type: application/json" -X POST localhost:5000/forums/1
```

Successful Response: 201 Created
Sucess: Thread and Post Created
Error: 404 Not Found

### 5.  GET /forums/<forum_id>/<thread_id>
Curl call: 
```curl localhost:5000/forums/1/1```
+ Response: Success 200 OK
+ Curl call: 
```
[
	{
	    "post_Id": 1,   
	    "post_authorid": 1,
	    "post_forumid": 1,
	    "post_text": "I am having trouble connectingto Redis. Do you have any idea how to do it?",
	    "post_threadId": 1,
	    "post_time": "2018-09-26 04:27:21"
	  }
]
```
### 6. POST /forums/<forum_id>/<thread_id>
Curl call: 
```curl -v -u holly:password -d '{"thread_title":"Love", "text": "I love you"}' -H "Content-Type: application/json" -X POST localhost:5000/forums/1
```

Successful Response: 201 Created
Sucess: Thread and Post Created
Error: 404 Not Found

### 7. POST /users

### 8. PUT /users/<username>

