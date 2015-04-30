from hashlib import md5
from app import db
from datetime import datetime

class Couple(db.Model):

    __tablename__ = 'couple'

    id = db.Column(db.Integer, primary_key=True)
    user_id_c1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_c2 = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, c1, c2):
        self.user_id_c1 = c1
        self.user_id_c2 = c2


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')
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
    def get_all_by_user_id(self, user_id):

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
