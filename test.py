from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

with app.app_context():
    db.create_all()
    user = User(id='1', username='admin', email='admin@example.com')
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    print(users)

@app.route('/')
def hello():
    return 'ok'

if __name__ == '__main__':
    app.run()
