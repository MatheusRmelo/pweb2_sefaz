from flask import Flask, render_template
from controller.user_controller import user_controller
from database import db

TEMPLATE = './templates'
STATIC = './static'

app = Flask(__name__, static_url_path='', template_folder=TEMPLATE, static_folder=STATIC)
app.register_blueprint(user_controller)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dbtest.db'
db.init_app(app)

with app.app_context():
  db.create_all()

@app.route("/")
def login():
  return render_template("login.html")

@app.route("/login", methods=['POST'])
def home():
  return render_template("index.html")

app.run()