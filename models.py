from google.appengine.ext import ndb

class Message(ndb.model):
    message = ndb.StringProperty()