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

### 1. Get /forums
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
### 2. Post /forums
Curl call: 
```curl -v -u holly:password -d '{"forum_name":"HTML"}' -H "Content-Type: application/json" -X POST localhost:5000/forums```

Response: 
Error: 409 for duplicate forum names
Success: Success: forum created

### 3.  Get /forums/<form_id>
Curl call: 
```curl localhost:5000/forums/1```

Response: 
Curl call: 
```
[
	{
		"Id": 1,
		"forum_creator": "alice",
		"forum_name": "redis"
	}
]
```
