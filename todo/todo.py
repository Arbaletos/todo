import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash 

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'todo.db'),
  SECRET_KEY='disvolvigxa sxlosilo',
  USERNAME='admin',
  PASSWORD='derparol'
))

app.config.from_envvar('TODO_SETTINGS', silent=True)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/list', methods=['GET'])
def tasklist():
  db = get_db()
  cur = db.execute('select task, done, id from tasks order by id desc')
  tasks = [[i['id'],i['task'],i['done']] for i in cur.fetchall()]
  return json.dumps(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    action('insert into tasks (task, done) values (?, ?)',
                 [json.loads(request.data.decode())['task'], 0])
    return redirect(url_for('tasklist'))

@app.route('/ch', methods=['POST'])
def change():
  action('update tasks set done=abs(done-1) where id=?',[json.loads(request.data.decode())['id']])
  return redirect(url_for('tasklist'))

@app.route('/del', methods=['POST'])
def delete():
  action('delete from tasks where id=?',[json.loads(request.data.decode())['id']])
  return redirect(url_for('tasklist'))

@app.route('/drop', methods=['POST'])
def drop():
  action('delete from tasks', None)
  return redirect(url_for('tasklist'))

def action(st, tem):
  db = get_db()
  cur = db.execute(st,tem)
  db.commit()
  

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



