import flask
from flask import request, jsonify, render_template, json, abort, Response, flash, g
from flask_basicauth import BasicAuth
from flask.cli import AppGroup
# from flask_httpauth import HTTPTokenAuth
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

#Function using for query database
#Fetch each data one by one based on the query provided
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

    
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


@app.route('/forums', methods = ['GET'])
def api_forums():
    all_forums = query_db('SELECT * FROM forums;')
    return jsonify(all_forums)

@app.route('/forums/<int:forum_id>', methods = ['GET'])
def api_threads(forum_id):
    all_threads = query_db("SELECT * FROM threads where forum_id= ?;", [forum_id])
    return jsonify(all_threads)

# @app.route('/forums', methods=['POST'])
# @basic_auth.required
# def forums():
#     name = request.values['name']
#     creator = 'holly'
#     print(name)
#     conn = sqlite3.connect('discussionform.db')
#     conn.row_factory = lambda cursor, row: row[0]
#     cur = conn.cursor()
#     forum_names = cur.execute('SELECT name from forums').fetchall()
#
#     print(forum_names)
    # for forum_name in forum_names:
    #    if forum_name == name:
    #        return '<h1> 409 Conflict if forum already exists </h1>'
    #

    # cur.execute('''insert into forums (name, creator) values (?, ?)''',[name, creator])
  #   conn.commit()
  #   print('Successfully')
  #   return render_template()
    # return forums
    
if __name__ == "__main__":
    app.run(debug=True)