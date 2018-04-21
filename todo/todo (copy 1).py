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
  db = get_db()
  cur = db.execute('select task, done, id from tasks order by id desc')
  tasks = [[i['id'],i['task'],i['done']] for i in cur.fetchall()]
  return render_template('index.html',tasks=tasks)

@app.route('/drop', methods=['POST'])
def drop():
  db = get_db()
  cur = db.execute('delete from tasks')
  db.commit()
  return redirect(url_for('tasklist'))

@app.route('/list')
def tasklist():
  db = get_db()
  cur = db.execute('select task, done, id from tasks order by id desc')
  tasks = cur.fetchall()
  return render_template('tasklist.html',tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
  data = json.loads(request.data.decode())
  task = data['task']
  db = get_db()
  db.execute('insert into tasks (task, done) values (?, ?)', [task, 0])
  db.commit()
  return redirect(url_for('tasklist'))

"""
@app.route('/add', methods=['POST'])
def add_task():
    db = get_db()
    db.execute('insert into tasks (task, done) values (?, ?)',
                 [request.form['task'], 0])
    db.commit()
    #flash('New task added')
    return redirect(url_for('index'))
"""

@app.route('/act', methods=['POST'])
def act():
    db = get_db()
    if request.form['action']=='drop':
      db.execute('delete from tasks where id=?',[request.form['id']])
      db.commit()
      flash('Task deleted')
    elif request.form['action']=='change':
      db.execute('update tasks set done=abs(done-1) where id=?',[request.form['id']])
      db.commit()
      flash('Task updated')
    return redirect(url_for('index'))

"""
@app.route('/')
def show_tasks():
    db = get_db()
    cur = db.execute('select task, done from tasks order by id desc')
    tasks = cur.fetchall()
    return render_template('tasks.html', tasks=tasks)
"""

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



