from flask import Flask, request
from flask_restful import Api, Resource
from backend.movies import Movie_list

app = Flask(__name__)
api = Api(app)

class flims(Resource):
    def get(self,id):
        return "Hai Hello All"

    def post(self):
        new_movie = Movie_list(
            title = request.json['title']
        )
        return "success"

api.add_resource(flims, '/api/movies/<int:id>/')          