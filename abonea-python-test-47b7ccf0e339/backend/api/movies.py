import time

from backend.wsgi import remote, messages, message_types

from backend import api, movies,user
from backend.oauth2 import oauth2, Oauth2
from backend.swagger import swagger
from .data import Data



class CreateRequest(messages.Message):
    Title = messages.StringField(1, required=True)
    imdbID = messages.StringField(2)
    Year = messages.StringField(3, required=True)
    Type = messages.StringField(4)
    Poster = messages.StringField(5)



class TokenRequest(messages.Message):
    access_token = messages.StringField(1, required=True)
    refresh_token = messages.StringField(2, required=True)


class TokenResponse(messages.Message):
    access_token = messages.StringField(1)
    expires = messages.FloatField(2)
    refresh_token = messages.StringField(3)


class LoginRequest(messages.Message):
    email = messages.StringField(1)
    password = messages.StringField(2)


class GetRequest(messages.Message):
    Title = messages.StringField(1, required=True)


class GetResponse(messages.Message):
    Title = messages.StringField(1, required=True)
    imdbID = messages.StringField(2)
    Year = messages.StringField(3, required=True)
    Type = messages.StringField(4)
    Poster = messages.StringField(5)


class MeResponse(messages.Message):
    Title = messages.StringField(1)
    imdbID = messages.StringField(2)
    type = messages.StringField(3)
    Poster = messages.StringField(4)
    Year = messages.StringField(5)


class SearchResult(messages.Message):
    Title = messages.StringField(1)
    imdbID = messages.StringField(2)


class SearchResponse(messages.Message):
    movies = messages.MessageField(SearchResult, 1, repeated=True)

class UpdateRequest(messages.Message):
    Title = messages.StringField(1)
   
class DeleteRequest(messages.Message):
    Title = messages.StringField(1)

@api.endpoint(path="movies", title="Movies API")
class Movies(remote.Service):
    @swagger("Get a movies")
    @remote.method(GetRequest, GetResponse)
    def get(self, request):
        movie = movies.Movie_list.get_by_tittle(request.title)
        return GetResponse(
            movie.Title,
            movie.imdbID,
            movie.Year,
            movie.Type,
            movie.Poster
            #id='1',
            #name='test'
        )

    @swagger("Create a Movies")
    @oauth2.required()
    @remote.method(CreateRequest, TokenResponse)
    def create(self, request):
        mov = movies.Movie_list.create(Title= request.title, imdbID=request.imdbid, Year=request.year, Type=request.type, Poster=request.poster)
        session = Oauth2.create(mov.key)

        return TokenResponse(
            access_token=session.access_token.token,
            expires=time.mktime(session.access_token.expires.timetuple()),
            refresh_token=session.refresh_token.token
        )
    
    @swagger("Add New a Movie")
    @oauth2.required()
    @remote.method(CreateRequest, TokenResponse)
    def Add(self,request):
        Dict_data = Data().get_movie_by_title(request.title)
        result = mov = movies.Movie_list.create(Title= request.title, imdbID=request.imdbid, Year=request.year, Type=request.type, Poster=request.poster)

        session = Oauth2.create(mov.key)

        return TokenResponse(
            access_token=session.access_token.token,
            expires=time.mktime(session.access_token.expires.timetuple()),
            refresh_token=session.refresh_token.token
        )

    @swagger("Insert bulk movies")
    @oauth2.required()
    @remote.method(CreateRequest, message_types.VoidMessage)
    def create_all(self):
        if movies.Movie_list.get_db_status:
            Dict_data = Data().final_data()
            for item in Dict_data:
                """title=item['Title']
                year=item['Year']
                poster=item['Poster']
                imdbID=item['imdbID']
                type=item['Type']"""
                result = movies.Movie_list.create_all(item)
                print("Inserted Entity into NDB: ", result)
                return message_types.VoidMessage()


    @swagger("Delete particular movie by particular user")
    @oauth2.required()
    @remote.method(DeleteRequest)
    def Delete_movie(self,request):
        if user.User.email == 'test@gmail.com':
            result = movies.Movie_list.delete_movie(request.imdbID)
            print("Deleted particular entry of item:{}".format(result))
            return message_types.VoidMessage()
        else:
            raise movies.EmailTaken("Invalid user:{} to do Delete".format(user.User.email))  