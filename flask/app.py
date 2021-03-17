from model.user import User
from flask import Flask, render_template, request
from controller.user_controller import user_controller
from database import db
from flask_login import login_user, logout_user
from login.login_manager import login_manager
from flask_login import current_user

TEMPLATE = './templates'
STATIC = './static'

app = Flask(__name__, static_url_path='', template_folder=TEMPLATE, static_folder=STATIC)
app.register_blueprint(user_controller)

login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dbtest.db'
db.init_app(app)

app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

with app.app_context():
  db.create_all()

@app.route("/")
def login():
  if not hasattr(current_user, 'id'):
    return render_template("login.html")
  else:
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def home():
  error = None
  if request.method == 'POST':
    users = User.query.filter_by(email=request.form['username'])
    if not users.first() == None:
      user = users.first()
      if user.password == request.form['password']:
        login_user(user, remember=True)
        return render_template('index.html') 
      else:
        error = 'Invalid Credentials. Please try again.'
    else:
      error = 'Invalid Credentials. Please try again.'
  return render_template('login.html', error=error)

@app.route("/logout", methods=['GET'])
def logout():
  logout_user()
  return render_template('login.html')

app.run()