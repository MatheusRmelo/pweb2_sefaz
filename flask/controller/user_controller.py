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

@user_controller.route("/store", methods=['POST'])
@login_required
def add_location():
  HEADERS = {
      "appToken": '82920d4042d310a817206770bd9afa852976f129',
      "Content-Type": "application/json"
  }
  URL = 'http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecosPorCodigoDeBarras'


  cestaBasica = [
    {'name':'arroz','codigo':'7896006755517'},
    {'name':'oleo','codigo': '7891107101621'},
    {'name':'feijao','codigo': '7898902735167'}
  ]
  listaMelhores = []
  listaLojas = []
  for i in cestaBasica:
    data = {
      "codigoDeBarras": i['codigo'],
      "dias": 3,
      "latitude": -9.6432331,
      "longitude": -35.7190686,
      "raio": 15
    }
    r = requests.post(url= URL, data=json.dumps(data), headers = HEADERS)
    result = r.json()
    cont = 0 
    if len(result) >= 10:
      cont = 10
    else:
      cont = len(result)
      
    for x in range(cont): 
      loja = {
        'price': result[x]['valUltimaVenda'],
        'name': result[x]['nomRazaoSocial'],
        'items': [result[x]['dscProduto']]
      }
      if i['name'] == 'arroz':
        print('----------------------------------------' + result[x]['nomRazaoSocial'])
        listaMelhores.append(loja)
        listaLojas.append(result[x]['nomRazaoSocial'])
      else:
        try:
          listaMelhores[listaLojas.index(result[x]['nomRazaoSocial'])]['price'] = listaMelhores[listaLojas.index(result[x]['nomRazaoSocial'])]['price'] + result[x]['valUltimaVenda']
          listaMelhores[listaLojas.index(result[x]['nomRazaoSocial'])]['items'].append(result[x]['dscProduto'])
        except:
          print('Loja não possui um dos valores')
  

  for validLojas in listaMelhores:
    if(len(validLojas['items']) != len(cestaBasica)):
      listaMelhores.remove(validLojas)
      print('removeu')
      print(validLojas)
    print('passou')
    print(validLojas)


  print('----------------------------------')
  print(listaMelhores)
  print('----------------------------------')

  return render_template("store.html", listaMelhores = listaMelhores, items = listaMelhores[0]['items'])

@user_controller.route("/store")
@login_required
def store():
  return render_template("store.html")
