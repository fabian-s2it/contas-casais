from hashlib import md5
from app import db

class Couple(db.Model):

    __tablename__ = 'couple'

    user_id_c1 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_id_c2 = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __init__(self, c1, c2):
        self.user_id_c1 = c1
        self.user_id_c2 = c2


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def passwordify(self):
        self.password = (md5(self.email.encode('utf-8')).hexdigest(), 18)

    def create_couple(self, couple_id):
        couple = Couple(self.id, couple_id)
        db.session.add(couple)
        db.session.commit()

    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'username': self.username,
           'email': self.email,
           'password': self.password
       }

    # @property
    # def serialize_many2many(self):
    #    """
    #    Return object's relations in easily serializeable format.
    #    NB! Calls many2many's serialize property.
    #    """
    #    return [ item.serialize for item in self.many2many]

class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def passwordify(self):
        self.password = (md5(self.email.encode('utf-8')).hexdigest(), 18)

    def create_couple(self, couple_id):
        couple = Couple(self.id, couple_id)
        db.session.add(couple)
        db.session.commit()

    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'username': self.username,
           'email': self.email,
           'password': self.password
       }

class CoupleTransaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def passwordify(self):
        self.password = (md5(self.email.encode('utf-8')).hexdigest(), 18)

    def create_couple(self, couple_id):
        couple = Couple(self.id, couple_id)
        db.session.add(couple)
        db.session.commit()

    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'username': self.username,
           'email': self.email,
           'password': self.password
       }

