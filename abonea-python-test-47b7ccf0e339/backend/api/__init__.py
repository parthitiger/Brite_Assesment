from email.mime import base
import pkgutil
import os
from backend import wsgi
from .api import app as flaskapp
 

class Application(wsgi.Application):
    pass


application = Application(base_path="api")
print(application)
print(dir(application))
#application.app = app
print('Appli',application.app)
service = application.service
print('--****',service)
#print(type(service))
endpoint = application.service
print('**---',endpoint)

for _, modname, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
    #print(_,modname)
    __import__(modname)
