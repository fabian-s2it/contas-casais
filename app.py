from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/contas'

auth = HTTPBasicAuth()

db = SQLAlchemy(app)
api = restful.Api(app)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return True
    return None


class Users(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    @auth.login_required
    def get(self, user_id):
        user = User.query.get(user_id)
        return user.serialize


class UserList(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('password', type=str)

    def post(self):
        args = self.parser.parse_args()
        user = User(args['username'], args['email'], args['password'])

        db.session.add(user)
        db.session.commit()

        return True, 200


class Transactions(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int)
        self.parser.add_argument('category', type=int)
        self.parser.add_argument('type', type=int)
        self.parser.add_argument('amount', type=float)
        self.parser.add_argument('description', type=str)



    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        transaction = Transaction(args['user_id'], args['category'], args['type'],
                                  args['amount'], args['description']
                                 )

        db.session.add(transaction)
        db.session.commit()

api.add_resource(Users, '/users/<user_id>')
api.add_resource(UserList, '/user/')
api.add_resource(Transactions, '/transaction/')

if __name__ == '__main__':
    app.run(debug=True, port=2323)