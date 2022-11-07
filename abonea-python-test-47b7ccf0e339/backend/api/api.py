from flask import Flask, request, jsonify, Response

from .data import Data
from backend import movies
from .movies import Movies

# Test Application design

app = Flask(__name__)

class api:
    @app.route('/api/test', methods=['GET', 'POST'])
    def test(self):
        if request.method == 'POST':
            return jsonify(**request.json)
        return "Hello World"

    @app.route('/api/user', methods=['GET','POST']) 
    def users(self):
        if request.method == 'POST':
            return jsonify(**request.json)
        return 'Hello User'    

    @app.route('/api/movies/create_movies', methods=['GET','POST'])
    def Movie_operation(self):
        if request.method == 'POST':
            data = request.args
            return Movies.create(request)

    @app.route('/api/movies/get_movies_by_title', methods=['GET','POST'])
    def Movie_operation(self):
        if request.method == 'POST':
            data = request.args
            return Movies.get(request)     

    @app.route('/api/movies/add_movies', methods=['GET','POST'])
    def Movie_operation(self):
        if request.method == 'POST':
            data = request.args
            return Movies.Add(request)        

    @app.route('/api/movies/delete_movies', methods=['GET','POST'])
    def Movie_operation(self):
        if request.method == 'POST':
            data = request.args
            return Movies.Delete_movie(request)

    @app.route('api/movies/movie_title', methods=['GET'])
    def Get_movie_from_title(movie_title):
        return Movies.get(movie_title)


    def __call__(self):
        return app