import flask
from flask import request, jsonify, make_response, abort, Response
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

basic_auth = BasicAuth(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Function to query database
#Fetch each data one by one based on the query provided
def query_db(query, args=(), one=False):
    print(query)
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    fetch = cur.execute(query)
    return fetch
    # return (fetch[0] if fetch else None) if one else fetch

#Function connecting to database
def get_db():
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    return conn

@app.route('/forums', methods=['GET'])
def get_forums():
    query = 'SELECT * FROM forums'
    forums = query_db(query)
    return jsonify(forums)

@app.route('/forums', methods=['POST'])
# @basic_auth.required
def post_forums():

    name = request.values['name']
    creator = 'holly'
    print(name)
    query = 'SELECT name FROM forums'
    forum_names = query_db(query)
    print(forum_names)
    for forum_name in forum_names:
        # print(forum_name)
        # print(forum_name['name'])
        if forum_name['name'] == name:
           return duplicate_name(name)
   
    db = get_db()
    db.execute('insert into forums (name, creator) values (?, ?)',(name, creator))
    db.commit()

    return jsonify(forum_names)
    
@app.errorhandler(409)
def duplicate_name(name):
    return "<h1>409</h1><p>A forum already exists with the name " + name + ".</p>", 409

# @app.errorhandler(404)
# def thread_404(e, forum_id):
    # return "<h1>404</h1><p>No forum exists with the forum id of " + str(forum_id) + ".</p>", 404

@app.route('/forums/<int:forum_id>', methods=['GET'])
def get_threads(forum_id):
    print(forum_id)
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # Select from forums on forum id to make sure that the forum exists
    query = 'SELECT * FROM forums WHERE id = ' + str(forum_id)
    forum = cur.execute(query).fetchall()
    if len(forum) == 0:
        return  "<h1>404</h1><p>No forum exists with the forum id of " + str(forum_id) + ".</p>", 404
    # If forum exists, then select from threads where forum_id is equal to forum_id from api call
    query = 'SELECT * FROM threads WHERE forum_id = ' + str(forum_id) + ' ORDER BY timestamp DESC'
    threads = cur.execute(query).fetchall()
    return jsonify(threads)

app.run()