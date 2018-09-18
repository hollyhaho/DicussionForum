import flask
from flask import request, jsonify, render_template, json, abort, Response, flash, g, make_response
from flask_basicauth import BasicAuth
from flask.cli import AppGroup
import click
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'hoa'
app.config['BASIC_AUTH_PASSWORD'] = 'a'

basic_auth = BasicAuth(app)

DATABASE = './init.db'

#Function Connect Database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Function  execute script
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#Create Command initdb
#To use command, run in terminal export FLASK_APP = appname, flask initdb
@app.cli.command('init_db')
def initdb_command():
    init_db()
    print('Initialize the database.')        

#
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
#Function using for query database
#Fetch each data one by one based on the query provided
def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn. cursor()
    fetch = cur.execute(query).fetchall()
    return fetch
    
    
#Notify error with status code, response and reason
def notify_error(status_code, response, reason):
    notify = jsonify({
    "status" : status_code,
    "response": response,
    "reason": reason
    })
    return notify
    
#Get information based on username    
def get_credentials(username):
    user_name = query_db('''SELECT username FROM USER WHERE username =?''', [username], one=True)
    password = query_db('''SELECT password FROM USER WHERE username =?''', [username], one=True)
    app.config['BASIC_AUTH_USERNAME'] = user_name[0]
    app.config['BASIC_AUTH_PASSWORD'] = password[0]
    print(user_name)
    print(password)     
         
#Create User
@app.route('/users', methods=['GET','POST'])
def register(): 
      if request.method == 'POST':
          if not request.form['username'] or not request.form['password']:
              return notify_error(400,'Bad Request','Username or password is not entered')
          
          #check duplicated username
          cur = query_db('select ID from user where username=?', [request.form['username']], one=True)
          if cur is not None:
              return notify_error(409, 'Conflict', 'Username already exists')
          else: 
              db = get_db()
              db.execute('insert into user(username, password) values (?,?)', [request.form['username'], request.form['password']])
              db.commit()
              return render_template('signup.html', username=request.form['username'], password=request.form['password'])
      else:
          return render_template('signup.html')

#List available discussion forums
@app.route('/forums', methods = ['GET'])
def api_forums():
    all_forums = query_db('SELECT forums.Id, forums.forum_name, user.username FROM  forums INNER JOIN user ON forums.Id = user.Id ;')
    return jsonify(all_forums)

#List threads in the specified forum
@app.route('/forums/<int:forum_id>', methods = ['GET'])
def api_threads(forum_id):
    query = 'SELECT Id FROM forums WHERE Id = ' + str(forum_id) +';'
    forum = query_db(query)
    if not forum :
        return notify_error(404, 'Error', 'No forum exists with the the forum id of ' + str(forum_id))   
    else:
        query = 'SELECT threads.Id, threads.thread_title, threads.thread_time, user.username as creator FROM user, threads  where  forum_Id = ' + str(forum_id) +' AND threads.thread_creator = user.Id ORDER BY thread_time DESC;'
        threads = query_db(query)
        return jsonify(threads)
        
#List posts in the specified thread
# @app.route('/forums/<int:forum_id>/<thread_id>', methods = ['GET'])
# def api_posts(thread_id):
    
    
if __name__ == "__main__":
    app.run(debug=True)