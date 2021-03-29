import requests
import json
from flask import render_template, Blueprint, request, redirect
from model.user import User, Role
from flask_login.utils import login_required
from login.decorators import admin_login_required
from flask_login import current_user

TEMPLATE = './templates'
STATIC = './static'

user_controller = Blueprint('users', __name__, static_url_path='', template_folder=TEMPLATE, static_folder=STATIC)

@user_controller.route("/userForm")
@login_required
def userForm():
  return render_template("users/user.html", roles=Role.query.all())

@user_controller.route("/users")
@login_required
def users():
  users = User.query.all()
  return render_template("users/users.html", users=users)

@user_controller.route("/users", methods=['POST'])
@login_required
def add_user():
  name = request.form.get('name')
  email = request.form.get('email')
  jobTitle = request.form.get('jobTitle')
  password = request.form.get('password')
  roles = request.form.get('roles')
  
  user = User(email, name, jobTitle, password, [Role.query.filter_by(id=roles[0]).first()])
  user.save()

  return redirect("/users")

@user_controller.route("/roles", methods=['POST'])
@login_required
def add_role():
  name = request.form.get('name')
  description = request.form.get('description')
  
  role = Role(name, description)
  role.save()

  return redirect("/roles")

@user_controller.route("/roles")
@login_required
def roles():
  roles = Role.query.all()
  return render_template("users/roles.html", roles=roles)

@user_controller.route("/roleForm")
@login_required
def roleForm():
  return render_template("users/role.html")

def searchFirstItem(codigo):
  HEADERS = {
      "appToken": '82920d4042d310a817206770bd9afa852976f129',
      "Content-Type": "application/json"
  }
  URL = 'http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecosPorCodigoDeBarras'

  data = {
    "codigoDeBarras": codigo,
    "dias": 3,
    "latitude": -9.6432331,
    "longitude": -35.7190686,
    "raio": 15
  }
  r = requests.post(url= URL, data=json.dumps(data), headers = HEADERS)
  cont = 0 
  if len(result) >= 10:
    cont = 10
  else:
    cont = len(result)
  
  lojas = []
  for i in range(cont):
    loja = {
      'price': result[i]['valUltimaVenda'],
      'name': result[i]['nomRazaoSocial'],
      'cnpj': result[i]['numCNPJ']
    }
    lojas.append(loja)

  return lojas

def searchItemEmp(codigo, cnpj):
  HEADERS = {
      "appToken": '82920d4042d310a817206770bd9afa852976f129',
      "Content-Type": "application/json"
  }
  URL = 'http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecoProdutoEmEstabelecimento'
  data = {
    "cnpj": cnpj,
    "codigoBarras": codigo,
    "quantidadeDeDias": 3
  }
  r = requests.post(url= URL, data=json.dumps(data), headers = HEADERS)

  return r['valUltimaVenda']



@user_controller.route("/store", methods=['POST'])
@login_required
def add_location():
  cestaBasica = [
    {'name':'arroz','codigo':'7896006755517'},
    {'name':'oleo','codigo': '7891107101621'},
    {'name':'feijao','codigo': '7898902735167'}
  ]
  listaMelhores = []
  for i in len(cestaBasica):
    if i == 1:
      listaMelhores = searchFirstItem(i['codigo'])
    else:
      for loja in listaMelhores:
        loja['price'] = loja['price'] + searchItemEmp(codigo, loja['cnpj']) 
  print('---------------------------')      
  print(listaMelhores)
  print('---------------------------')      
  return render_template("store.html", listaMelhores = listaMelhores)

@user_controller.route("/store")
@login_required
def store():
  return render_template("store.html")
