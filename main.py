import flask
from flask import request, jsonify, make_response, abort, Response, g, current_app
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True

class Authentication(BasicAuth):
    def check_credentials(self, username, password):
        print('check_credentials')
        # query from database 
        query = "SELECT * from user where username ='{}'".format(username)
        user = query_db(query)
        if user == []:
            return False
        if user[0]['password'] == password:
            current_app.config['BASIC_AUTH_USERNAME'] = username
            current_app.config['BASIC_AUTH_PASSWORD'] = password
            return True
        else: 
            return False
       

basic_auth = Authentication(app)
DATABASE = './discussionforum.db'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    fetch = cur.execute(query).fetchall()
    return fetch


@app.route('/forums', methods=['GET'])
def get_forums():
    query = "SELECT * FROM forums;"
    forums = query_db(query)
    return jsonify(forums)

@app.route('/forums', methods=['POST'])
@basic_auth.required
def post_forums():

    data = request.get_json(force=True)
    name = data['forum_name']

    creator = current_app.config['BASIC_AUTH_USERNAME']
    query = 'SELECT forum_name FROM forums'
    forum_names = query_db(query)
    for forum_name in forum_names:
        if forum_name['forum_name'] == name:
            error = '409 A forum already exists with the name ' + name
            return make_response(jsonify({'error': error}), 409)
   
    db = get_db()
    db.execute('insert into forums (forum_name, forum_creator) values (?, ?)',(name, creator))
    db.commit()

    query = "select id from forums where forum_name ='{}'".format(name)
    new_forum = query_db(query)
    response = make_response('Success: forum created')
    response.headers['location'] = '/forums/{}'.format(new_forum[0]['id'])
    response.status_code = 201

    return response
    

@app.route('/forums/<int:forum_id>', methods=['GET'])
def get_threads(forum_id):
    # Select from forums on forum id to make sure that the forum exists
    query = 'SELECT * FROM forums WHERE id = ' + str(forum_id)
    forum = query_db(query)
    print(forum)
    if len(forum) == 0:
        error = '404 No forum exists with the forum id of ' + str(forum_id)
        return make_response(jsonify({'error': error}), 404)
    # If forum exists, then select from threads where forum_id is equal to forum_id from api call
    query = 'SELECT * FROM threads WHERE forum_id = ' + str(forum_id) + ' ORDER BY thread_time DESC'
    # threads = cur.execute(query).fetchall()
    threads = query_db(query)
    return jsonify(threads)


@app.route('/forums/<int:forum_id>', methods=['POST'])
@basic_auth.required
def post_thread(forum_id):

    data = request.get_json(force=True)
    title = data['thread_title']
    text = data['text']
    creator = current_app.config['BASIC_AUTH_USERNAME']

     # Select from forums on forum id to make sure that the forum exists
    query = 'SELECT * FROM forums WHERE id = ' + str(forum_id)
    forum = query_db(query)
    print(forum)
    if len(forum) == 0:
        error = '404 No forum exists with the forum id of ' + str(forum_id)
        return make_response(jsonify({'error': error}), 404)
    # If forum exist, insert into threads table
    db = get_db()
    db.execute('insert into threads (thread_title, thread_creator, forum_Id) values (?, ?, ?)',(title, creator, str(forum_id)))
    db.commit()
    # Get the thread_id from the new thread to put into post's thread_id
    file_entry = query_db('SELECT last_insert_rowid()')
    thread_id = file_entry[0]['last_insert_rowid()']
    # Insert text as a new post
    db.execute('insert into posts (post_text, post_authorid , post_threadId) values (?, ?, ?)',(text, creator, str(thread_id)))
    db.commit()

    response = make_response("SUCCESS: THREAD CREATED")
    response.headers['location'] = '/forums/{}/{}'.format(str(forum_id), thread_id)
    response.status_code = 201
    return response

@app.route('/forums/<int:forum_id>/<int:thread_id>', methods=['GET'])
def get_post(forum_id, thread_id):
    print(forum_id, thread_id)
    response = {'forum_id': forum_id, 'thread_id': thread_id}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
