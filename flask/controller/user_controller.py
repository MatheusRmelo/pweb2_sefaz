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

def searchFirstItem(codigo, latitude, longitude):
  HEADERS = {
      "appToken": '82920d4042d310a817206770bd9afa852976f129',
      "Content-Type": "application/json"
  }
  URL = 'http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecosPorCodigoDeBarras'
  data = {
    "codigoDeBarras": codigo,
    "dias": 3,
    "latitude": latitude,
    "longitude": longitude,
    "raio": 15
  }
  r = requests.post(url= URL, data=json.dumps(data), headers = HEADERS)
  result = r.json()
  cont = 0 
  if len(result) >= 10:
    cont = 10
  else:
    cont = len(result)
  
  lojas = []
  print(result)
  try:
    valid = result[i]['valUltimaVenda']
  except:
    return lojas
  
  for i in range(cont):
    loja = {
      'price': result[i]['valUltimaVenda'],
      'name': result[i]['nomRazaoSocial'],
      'cnpj': result[i]['numCNPJ'],
      'items': [result[i]['dscProduto']]
    }
    try:
      lojas.index(loja)
    except:
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
  try: 
    result = r.json()
    return {
      'price': result['valUltimaVenda'],
      'item': result['dscProduto']
    }
  except:
    return False

def validStores(listStores, length):
  newList = []
  for i in range(len(listStores)):
    if len(listStores[i]['items']) == length: 
      newList.append(listStores[i])
   
  return newList

@user_controller.route("/store", methods=['POST'])
@login_required
def add_location():
  latitude = request.form['latitude']
  longitude = request.form['longitude']
  cestaBasica = [
    {'name':'arroz','codigo':'7896006755517'},
    {'name':'oleo','codigo': '7891107101621'},
    {'name':'feijao','codigo': '7898902735167'}
  ]
  listaMelhores = []
  for i in cestaBasica:
    if i['name'] == 'arroz':
      listaMelhores = searchFirstItem(i['codigo'], latitude, longitude)
    else:
      for loja in listaMelhores:
        news = searchItemEmp(i['codigo'], loja['cnpj'])
        if news == False :
          listaMelhores.remove(loja)
        else:
          loja['price'] = loja['price'] + news['price']
          loja['items'].append(news['item'])

  listaMelhores = validStores(listaMelhores, len(cestaBasica))

  print('---------------------------')      
  print(listaMelhores)
  print('---------------------------')      

  return render_template("store.html", listaMelhores = listaMelhores)

@user_controller.route("/store")
@login_required
def store():
  return render_template("store.html")
