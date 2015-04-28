from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from hashlib import md5
from app import db
import json

couple = db.Table('couple',
	db.Column('user_id_c1', db.Integer, db.ForeignKey('user.id')),
	db.Column('user_id_c2', db.Integer, db.ForeignKey('user.id'))
)

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

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'username': self.username,
           'email': self.email,
           'password': self.password
       }
    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]


