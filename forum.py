import flask
from flask import request, jsonify, render_template
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

basic_auth = BasicAuth(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Function using for query database
#Fetch each data one by one based on the query provided
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    exc = cur.execute(query)
    fetch = exc.fetchall()
    return (fetch[0] if fetch else None) if one else fetch
    
#Function connecting to database
def get_db():
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    return conn
    
#Notify error with status code, response and reason
def notify_error(status_code, response, reason):
    notify = jsonify({
    "status" : status_code,
    "response": response,
    "reason": reason
    })
    return notify
    
#Create User
@app.route('/users', methods=['GET','POST'])
def register(): 
      if request.method == 'POST':      
          db = get_db()
          db.execute('insert into user(username, password) values (?,?)', [request.form['username'], request.form['password']])
          db.commit()
          return render_template('signup.html', username=request.form['username'], password=request.form['password'])
      else:
          return render_template('signup.html')
        
        
# A route to return all the available entries in our catalog
# @app.route('/forums', methods = ['POST','GET'])
# def api_forums():
#     all_forums = query_db('SELECT * FROM forums;')
#     return jsonify(all_forums)
  #   else:
  #       db = get_db()
  #       db.execute('''insert into forums (name, creator) values (?, ?)''',  [data['name'], data['creator']])
  #       db.commit()
  
        
# @app.route('/forums', methods=['POST'])
# def forums():
#     return render_template('signup.html', )

# @app.route("/")
# def hello():
#     return render_template('signup.html')
#
# @app.route("/echo", methods=['POST'])
# def echo():
#     return "You said: " + request.form['username'] + request.form['password']
    
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