import flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import db


if __name__ == '__main__':
    def create_app():
        app = flask.Flask("app")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/contas'
        db.init_app(app)
        with app.app_context():
            # Extensions like Flask-SQLAlchemy now know what the "current" app
            # is while within this block. Therefore, you can now run........
            db.create_all()

        return app

    #create_app()
