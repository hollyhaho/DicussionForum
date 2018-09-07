import flask
from flask import request, jsonify
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# A route to return all the available entries in our catalog
@app.route('/forums', methods=['GET'])
def api_forums():
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_forums = cur.execute('SELECT * FROM forums;').fetchall()

    return jsonify(all_forums)

@app.route('/forums', methods=['POST'])
@basic_auth.required
def forums():
    name = request.values['name']
    creator = 'holly'
    print(name)
    conn = sqlite3.connect('discussionform.db')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    forum_names = cur.execute('SELECT name from forums').fetchall()

    print(forum_names)
    for forum_name in forum_names:
       if forum_name == name:
           return '<h1> 409 Conflict if forum already exists </h1>'
    

    cur.execute('insert into forums (name, creator) values (?, ?)',(name, creator))
    conn.commit()
    return "<h1>Test</h1>"
    # return forums
    

app.run()