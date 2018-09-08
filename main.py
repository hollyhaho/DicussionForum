import flask
from flask import request, jsonify, make_response, abort
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

@app.route('/forums', methods=['GET'])
def get_forums():
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_forums = cur.execute('SELECT * FROM forums;').fetchall()

    return jsonify(all_forums)

@app.route('/forums', methods=['POST'])
@basic_auth.required
def post_forums():

    name = request.values['name']
    creator = 'holly'
    print(name)
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    forum_names = cur.execute('SELECT name from forums').fetchall()

    for forum_name in forum_names:
       if forum_name == name:
           return duplicate_name(name)
    

    cur.execute('insert into forums (name, creator) values (?, ?)',(name, creator))
    conn.commit()
    print(forum_names)
    return ','.join(forum_names)
    
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
    # If forum exists, then select from threads where forum_id is equal to forum_id from api call
    query = 'SELECT * FROM threads WHERE forum_id = ' + str(forum_id) + ' ORDER BY timestamp DESC'
    threads = cur.execute(query).fetchall()
    print(len(threads))
    if len(threads) == 0:
        return "<h1>404</h1><p>No forum exists with the forum id of " + str(forum_id) + ".</p>", 404
    return jsonify(threads)

app.run()