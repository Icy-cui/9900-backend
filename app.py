from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
from flask_restx import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
api = Api(app,
          default="Methods",
          title="Charity Connect api",
          version="1.0",
          default_label="Methods to access data",
          description="This is a charity and sponsor website backend")
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)

user_ns = api.namespace('User_Account', path='/user', description='user login / register')

class Charity(db.Model):
    """
    this is charity table
    """
    __tablename__ = 'charity'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)

@user_ns.route('/register')
class Register(Resource):
    def post(self):
        new_account = Charity(name='charity1', email='12233@gmail.com', password='122344')
        db.session.add(new_account)
        db.session.commit()
        resp = make_response({
            "status": "ok",
            "message": "success"
        })
        all_data = Charity.query.all()
        for data in all_data:
            print(data.name, data.email)
        return resp

with app.app_context():
    # db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(port=6000)
