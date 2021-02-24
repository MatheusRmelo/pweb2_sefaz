from flask import render_template, Blueprint, request, redirect
from model.user import User, Role

TEMPLATE = './templates'
STATIC = './static'

user_controller = Blueprint('users', __name__, static_url_path='', template_folder=TEMPLATE, static_folder=STATIC)

@user_controller.route("/form")
def userForm():
  #admin = User(
  #  name='Flávio Medeiros', 
  #  email='admin@example.com', 
  #  jobTitle='Administrador', 
  #  roles=[Role.query.filter_by(id=1).first()]
  #)
  #addUser(admin)
  return render_template("users/user.html", roles=Role.query.all())

@user_controller.route("/users2")
def usersData():
  users = User.query.all()
  return render_template("users/users.html", users=users)

@user_controller.route("/users")
def users():
  users = User.query.all()
  return render_template("users/simple.html", users=users)

@user_controller.route("/users", methods=['POST'])
def add_user():
  name = request.form.get('name')
  email = request.form.get('email')
  jobTitle = request.form.get('jobTitle')
  roles = request.form.get('roles')
  
  user = User(email, name, jobTitle, [Role.query.filter_by(id=roles[0]).first()])
  user.save()

  return redirect("/users")