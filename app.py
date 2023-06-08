from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
from flask_restx import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
engine = create_engine("sqlite:///instance/test.db")
api = Api(app,
          default="Methods",
          title="Movie Connect api",
          version="1.0",
          default_label="Methods to access data",
          description="This is a Movie sharing website backend")
# 跨域
# CORS(app, supports_credentials=True)
db = SQLAlchemy(app)

user_ns = api.namespace('User_Account', path='/user', description='user login / register')

class User(db.Model):
    """
    this is user table
    """
    __tablename__ = 'user'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)

@user_ns.route('/register')
class Register(Resource):
    def post(self):
        new_account = User(name='user1', email='user11@gmail.com', password='122344')
        db.session.add(new_account)
        db.session.commit()
        resp = make_response({
            "status": "ok",
            "message": "success"
        })
        all_data = User.query.all()
        for data in all_data:
            print(data.name, data.email)
        return resp

@app.route('/init')
def init_database():
    db.drop_all(bind_key=None)
    db.create_all()
    db.session.commit()
    return 'ok'

if __name__ == '__main__':
    app.debug = True
    app.run()
