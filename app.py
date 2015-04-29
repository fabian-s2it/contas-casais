from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/contas'

auth = HTTPBasicAuth()

db = SQLAlchemy(app)
api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return True
    return None


class Users(Resource):
    @auth.login_required
    def get(self, user_id):
        user = User.query.get(user_id)
        return user.serialize


class UserList(Resource):
    def post(self):
        args = parser.parse_args()
        user = User(args['username'], args['email'], args['password'])

        db.session.add(user)
        db.session.commit()

        return True, 200

api.add_resource(Users, '/users/<user_id>')
api.add_resource(UserList, '/user/')

if __name__ == '__main__':
    app.run(debug=True, port=2323)