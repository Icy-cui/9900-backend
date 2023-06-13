from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class Hello(Resource):
    def get(self):
        return {'msg': 'hello'}

if __name__ == '__main__':
    app.run(debug=True)