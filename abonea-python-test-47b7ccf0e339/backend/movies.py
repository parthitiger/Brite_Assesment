from typing import Type

from google.cloud import ndb

from backend import error
import datetime


class NotFound(error.Error):
    pass

class EmailTaken(error.Error):
    pass

class Movie_list(ndb.Model):
    Title  = ndb.StringProperty()
    Year = ndb.StringProperty()
    Poster = ndb.StringProperty()
    imdbID = ndb.StringProperty()
    Type = ndb.StringProperty()
    

    def __init__(self, *args, **kwargs):
        super(Movie_list, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    @classmethod
    def create(cls, Title=None, Year=None, Poster=None, imdbID=None, Type=None):
        entity = cls(
            Title=Title,
            Year = Year,
            poster = Poster,
            imdbID= imdbID,
            Type = Type
        )
        entity.put()

        return entity

    @classmethod
    def create_all(cls, *args, **kwargs):
        
        entity = cls(
            Id = args['id'],
            Title= kwargs['Title'],
            Year = kwargs['Year'],
            poster = kwargs['Poster'],
            imdbID= kwargs['imdbID'],
            Type = kwargs['Type']
        )
        entity.put()

        return entity

    #Testing Purpose    
    @classmethod
    def get(cls, id):
        entity = ndb.Key(urlsafe=id).get()
        if entity is None or not isinstance(entity, cls):
            raise NotFound("No user found with id: %s" % id)
        return entity    

    @classmethod
    def get(cls,limit=None):
        if limit == None:
            entities = cls.query().order(cls.Title).fetch(10)
            
        else:
            entities = cls.query(().order(cls.Title)).fetch(limit=limit)    
            
        return entities 

    @classmethod
    def get_by_tittle(cls, title):
        entities = cls.query(cls.Title == title).fetch(1)
        return entities[0] if entities else None 

    @classmethod
    def get_db_status(cls):
        entity = cls.query(cls.Title).count()
        if entity is None :
            return True
        return False

    @classmethod
    def update_title(cls,src_title, des_title):
        entities = cls.query(cls.Title == src_title).fetch(1)
        entity = entities.get()
        entity.Title = des_title
        entities.put()

    @classmethod
    def delete_movie(cls,imdbID):
        entities = cls.query(cls.imdbID == imdbID).fetch(1)
        entities.delete()
