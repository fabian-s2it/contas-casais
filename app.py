from flask import Flask, jsonify
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse, abort, Api, Resource
from models import *
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/contas'

db = SQLAlchemy(app)
api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)

class Users(restful.Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return user.serialize


class UserList(restful.Resource):
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