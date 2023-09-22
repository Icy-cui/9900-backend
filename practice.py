import json
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
api = Api(app, default='method', title='Movie Connect API', version='1.0',
          description='This is a movie sharing website platform backend')
db = SQLAlchemy(app)
# 跨域处理
CORS(app, supports_credentials=True)

# namespace
user_ns = api.namespace('User_account', path='/user', description='user login /register')
movie_ns = api.namespace('Movie_data', path='/movie', description='movie information')


class User(db.Model):
    """
    User table
    - id
    - email
    - password
    - description
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True)
    email = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)


class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    img_link = db.Column(db.String(250), nullable=True)
    director = db.Column(db.String(50), nullable=False)
    writer = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)


class LinkedMovie(db.Model):
    __tablename__ = 'linkedMovie'
    link_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_valid = db.Column(db.Integer, default=1)


@user_ns.route('/register')
class Register(Resource):
    @user_ns.response(409, str({'message': 'Register fail: password confirmation error'}))
    @user_ns.response(400, str({'message': 'Register fail: the format of email error'}))
    @user_ns.response(201, str({'status': 'ok', 'message': 'success'}))
    @user_ns.response(200, str({'message': 'account already exists'}))
    @api.param('name', 'user name')
    @api.param('email', 'the email of user')
    @api.param('password1', 'the password of user')
    @api.param('password2', 'the confirm password of user')
    @api.param('description', "the user's description")
    def post(self):
        # Get parameters
        content = request.get_json()
        name = content["name"]
        email = content["email"]
        pwd1 = content["password1"]
        pwd2 = content["password2"]
        print(content)
        new_account = User(name=name, email=email, password=pwd1, description=pwd2)
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


@movie_ns.route('/getData')
class MovieInfo(Resource):
    @movie_ns.response(200, str({'message': 'success'}))
    @api.param('title', 'movie title')
    def get(self):
        # Get parameters
        keyword = request.args.get('title')
        print(keyword)
        # content = request.get_json()
        # keyword = content["title"]
        # query by title
        movie_detail = Movie.query.filter(Movie.title == keyword).first()
        # if build 404 pages, we can use this to solve 404
        # movie_detail = db.get_or_404(Movie, keyword)
        print(movie_detail)
        if movie_detail:
            response = {
                "message": "success",
                "title": movie_detail.title,
                "director": movie_detail.director,
                "writer": movie_detail.writer,
            }
        else:
            response = {
                "message": 'no such movie'
            }
        resp = make_response(response)
        return resp


@app.route('/init')
def init_database():
    db.create_all()
    # db.drop_all()
    db.session.commit()
    return 'ok'


@app.route('/addMovies')
def add_movies():
    # Opening JSON file
    f = open('./movies.json')
    # returns JSON object as a dictionary
    data = json.load(f)
    print(data['movies'])
    # Closing file
    f.close()
    for movie in data['movies']:
        new_movie = Movie(movie_id=movie['movie_id'], title=movie['title'], img_link=movie['img_link'],
                          director=movie['director'],
                          writer=movie['writer'], genre=movie['genre'], year=movie['year'],
                          description=movie['description'])
        db.session.add(new_movie)
        db.session.commit()
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)