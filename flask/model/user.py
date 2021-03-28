from database import db
from flask_login import UserMixin
from login.login_manager import login_manager

users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))
# store_prices = db.Table('store_price',
#     db.Column('store_id', db.Integer(), db.ForeignKey('prices.id')),
#     db.Column('price_id', db.Integer(), db.ForeignKey('stores.id')))
users_location = db.Table('user_location',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('location_id', db.Integer(), db.ForeignKey('locations.id')))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Role %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

# class Store(db.Model):
#     __tablename__ = 'stores'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))

#     def __init__(self, name):
#         self.name = name 

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

# class PriceStore(db.Model):
#     __tablename__ = 'prices'
#     id = db.Column(db.Integer, primary_key=True)
#     id_store = db.relationship('Store', secondary=store_prices, backref=db.backref('price', lazy='dynamic'))

#     def __init__(self, id_store):
#         self.id_store = id_store

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer(), primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    user = db.relationship('Location', secondary=users_location, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, latitude, longitude, user):
        self.latitude = latitude
        self.longitude = longitude
        self.user = user
    def save(self):
        db.session.add(self)
        db.session.commit()       

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    jobTitle = db.Column(db.String(80))
    password = db.Column(db.String(20))
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, name, jobTitle, password, roles):
        self.name = name
        self.email = email
        self.jobTitle = jobTitle
        self.password = password
        self.roles = roles

    def __repr__(self):
        return '<User %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_administrator(self):
        return True

    @login_manager.user_loader
    def user_loader(user_id):
        return User.query.filter_by(email=user_id).first()