from google.appengine.ext import db

class Email(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    date = db.DateTimeProperty()
    
class Lib(db.Model):
    email = db.ReferenceProperty(Email)
    original = db.StringProperty()
    position = db.IntegerProperty()
    description = db.StringProperty()