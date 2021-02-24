from database import db

users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    jobTitle = db.Column(db.String(80))
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, name, jobTitle, roles):
        self.name = name
        self.email = email
        self.jobTitle = jobTitle
        self.roles = roles

    def __repr__(self):
        return '<User %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()