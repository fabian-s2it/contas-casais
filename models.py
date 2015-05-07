from hashlib import md5, sha1
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
import os

db = SQLAlchemy()

class Couple(db.Model):

    __tablename__ = 'couple'

    id = db.Column(db.Integer, primary_key=True)
    user_id_c1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_c2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('CoupleTransaction', backref='couple_transaction', lazy='dynamic')

    def __init__(self, c1, c2):
        self.user_id_c1 = c1
        self.user_id_c2 = c2


    @property
    def serialize(self):

        user_id_c1 = User.query.get(self.user_id_c1)
        user_id_c2 = User.query.get(self.user_id_c2)

        return {
           'id'         : self.id,
           'user_id_c1': user_id_c1.serialize,
           'user_id_c2': user_id_c2.serialize
        }


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    last_login = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, default=datetime.now())
    token = db.Column(db.String(120), unique=True)
    token_expiration_date = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.passwordify(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def passwordify(self, password):
        return md5(password + self.email.encode('utf-8')).hexdigest()

    def check_password(self, password):
        encoded_password = md5(password + self.email.encode('utf-8')).hexdigest()

        if encoded_password == self.password:
            return True

        return None

    def create_couple(self, couple_id):
        couple = Couple(self.id, couple_id)
        db.session.add(couple)
        db.session.commit()


    @classmethod
    def generate_token(cls, user_id):

        token = sha1(os.urandom(128)).hexdigest()
        user = User.query.get(user_id)

        user.token = token
        user.token_expiration_date = datetime(year=2099, month=12, day=12, hour=0, minute=0, second=0)
        user.last_login = datetime.now()

        db.session.add(user)
        db.session.commit()

        return token

    @classmethod
    def verify_user_exists(cls, username, email):

        user = User.query.filter((User.username == username) | (User.email == email)).first()

        if not user:
            return False

        return True



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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.Integer)
    type = db.Column(db.Integer)
    amount = db.Column(db.Float)
    description = db.Column(db.String(120), unique=False)
    datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, category, type, amount, description):
        self.user_id = user_id
        self.category = category
        self.type = type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return '<Description %r>' % self.description

    @classmethod
    def get_all_by_user_id(cls, user_id):

        transaction_list = []
        user = User.query.get(user_id)

        for transaction in user.transactions.all():

            transaction_dict = {
                'id': transaction.id,
                'user_id': transaction.user_id,
                'user': user.serialize,
                'category': transaction.category,
                'type': transaction.type,
                'amount': transaction.amount,
                'description': transaction.description,
                'datetime': transaction.datetime.strftime('%m/%d/%Y')
            }

            transaction_list.append(transaction_dict)

        return transaction_list


    @property
    def serialize(self):
       return {
           'id': self.id,
           'user_id': self.user_id,
           'category': self.category,
           'type': self.type,
           'amount': self.amount,
           'description': self.description,
           'datetime': self.datetime.strftime('%m/%d/%Y')
       }

class CoupleTransaction(db.Model):

    __tablename__ = 'couple_transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.id'))
    category = db.Column(db.Integer)
    type = db.Column(db.Integer)
    amount = db.Column(db.Float)
    description = db.Column(db.String(120), unique=False)
    datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, couple_id, category, type, amount, description):
        self.user_id = user_id
        self.couple_id = couple_id
        self.category = category
        self.type = type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return '<Description %r>' % self.description


    @classmethod
    def get_all_by_couple_id(self, couple_id):

        transaction_list = []
        couple = Couple.query.get(couple_id)

        for transaction in couple.transactions.all():

            transaction_dict = {
                'id': transaction.id,
                'user_id': transaction.user_id,
                'couple': couple.serialize,
                'category': transaction.category,
                'type': transaction.type,
                'amount': transaction.amount,
                'description': transaction.description,
                'datetime': transaction.datetime.strftime('%m/%d/%Y')
            }

            transaction_list.append(transaction_dict)

        return transaction_list

    @property
    def serialize(self):
       return {
           'id': self.id,
           'user_id': self.user_id,
           'couple_id': self.couple_id,
           'category': self.category,
           'type': self.type,
           'amount': self.amount,
           'description': self.description,
           'datetime': self.datetime.strftime('%m/%d/%Y')
       }
