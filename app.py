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
profile_ns = api.namespace('Profile', path='/profile', description='get user profile')


class User(db.Model):
    """
    User table -- collect registered user information
    - cid: user id
    - email: user email
    - name: username
    - password: user password
    - description: user can set description
    """
    __tablename__ = 'user'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)


class Movie(db.Model):
    """
    Movie table -- all movie information
    - movie_id: give each movie a unique id
    - movie_name: movie name
    - img_link: movie poster image link
    - director: movie's director
    - description: movie's short description
    """
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(50), nullable=False, unique=False)
    img_link = db.Column(db.String(250), nullable=True)
    director = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True)


class LinkedMovie(db.Model):
    """
    LinkedMovie -- provide m2m relations with movies and users
    - link_id: provide each link a unique id
    - movie_id: movie id mapping with table 'movie'
    - user_id: user id mapping with
    - is_valid: check if this relation is valid
    """
    __tablename__ = 'linkedMovie'
    link_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.cid'))
    is_valid = db.Column(db.Integer, default=1)


@user_ns.route('/register')
class Register(Resource):
    @user_ns.response(409, str({'message': 'Register fail: password confirmation error'}))
    @user_ns.response(400, str({'message': 'Register fail: the format of email error'}))
    @user_ns.response(201, str({'status': 'ok', 'message': 'success'}))
    @user_ns.response(200, str({'message': 'account already exists'}))
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


# -----------------------------------
# User profile page
# --- name, email, movies, and description
# -----------------------------------
@profile_ns.route('/user')
class UserProfile(Resource):
    @profile_ns.response(400, str({"message": "No user is found by the email"}))
    @profile_ns.response(200, str({"name": "eg. Amstrong",
                                   "description": "eg. ...",
                                   "movies": "eg. [movie1, movie2]",
                                   "message": "success"}))
    @api.param('email', 'the email of user')
    def post(self):
        # Get parameters
        # content = request.get_json()
        content = {'email': '123gmail.com'}
        email = content["email"]
        # email = request.args.get('email')
        # Determine whether the user exists
        user_info = User.query.filter(User.email == email).first()
        if user_info:
            linked_id_list = []
            # get the user's ID
            the_ID = user_info.cid
            # deal with movies link
            movie_res = LinkedMovie.query.filter(LinkedMovie.user_id == the_ID, LinkedMovie.is_valid == 1).all()
            for item in movie_res:
                if item.link_id in linked_id_list:
                    pass
                else:
                    linked_id_list.append(item.movie_id)
            movie_name_res = Movie.query.filter(LinkedMovie.movie_id.in_(linked_id_list)).all()
            movie_list = []
            for item in movie_name_res:
                movie_list.append(item.movie_name)

            response = {
                "name": user_info.name,
                "description": user_info.description,
                "movies": movie_list,
                "message": "success",
            }
            resp = make_response(response)
            resp.status_code = 200
            return resp


@app.route('/init')
def init_database():
    # db.drop_all(bind_key=None)
    db.create_all()
    db.session.commit()
    return 'ok'


if __name__ == '__main__':
    app.debug = True
    app.run()
