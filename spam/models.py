"""
======
Models
======

File: spam/models.py

Classes used to represent Email and Lib objects in Spamlibs. These class objects
are related to two entity types in the Google AppEngine datastore. The only 
relationship between the two objects is that one Email entity contains many Lib
entities.
"""
from google.appengine.ext import db
import re

class Email(db.Model):
    """
    An email message, with a title, body, and date.
    """
    
    #: A one-line title of the email.
    title = db.StringProperty()
    
    #: A multi-line chunk of text that contains the body of the email.
    body = db.TextProperty()
    
    #: The date that this email was sent.
    date = db.DateTimeProperty()
    
    #: How well does this spam rate?
    rating = db.IntegerProperty()
    
    #: How many times has this spam been viewed?
    views = db.IntegerProperty()
    
class Lib(db.Model):
    """
    A lib represents a specific term in an email, the description of its part of 
    speech, and its position in the original email.
    """
    
    #: An email that this Lib belongs to.
    email = db.ReferenceProperty(Email)
    
    #: The original text.
    original = db.StringProperty()
    
    #: The position in the email body where this term starts.
    position = db.IntegerProperty()
    
    #: The description of the language term, as defined by NLTK.
    description = db.StringProperty()
