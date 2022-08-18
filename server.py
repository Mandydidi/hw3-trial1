import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

HOST = ''
PORT = 3306
USERNAME = 'admin'
PASSWORD = ''
DB = 'hw1_db'

# dialect + driver://username:passwor@host:port/database
DATABASEURI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOST, PORT, DB)

engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():
  return render_template("firstpage.html")


# search function
@app.route('/search', methods=['POST'])
def search():
  selected = request.form['search']
  print(selected)
  act = request.form['action']
  print(act)
  if selected == 'User':
    if act == 'Create':
      return render_template('users_create.html')


  '''
  cursor = g.conn.execute(sql)
  data = dict()
  for result in cursor:
    data[result[1]] = [result[2], result[0]]
  cursor.close()
  return render_template("result.html", data=data, selected=selected, value=value)
  '''

@app.route('/CreateUser', methods=['POST'])
def createUser():
  # Users(userId: (primary key), userName, userEmail, pwd, Preference: json, links: json)
  name = request.form['username']
  id = request.form['userid']
  email = request.form['useremail']
  pwd = request.form["userpassword"]
  addr = request.form["useraddress"]
  pref = request.form["userpreferences"]
  sql = "INSERT INTO users VALUES " + "('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(id, name, email, pwd, addr, pref, '{}')
  print(sql)
  cursor = g.conn.execute(sql)
  print('Inserted successfully!')
  rsp = Response('Inserted successfully!', status=200, content_type="application/json")
  cursor.close()
  return rsp



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=5000, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
