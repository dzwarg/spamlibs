from google.appengine.ext import db
import re

class Email(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    date = db.DateTimeProperty()
    
class Lib(db.Model):
    email = db.ReferenceProperty(Email)
    original = db.StringProperty()
    position = db.IntegerProperty()
    description = db.StringProperty()
    
class EmailRequest(object):
    headers = {}
    bodies = {}
    header_item = re.compile('^([\w\-]+): (.*?)[\r\n]?$')
    header_break = re.compile('^\s+$')
    
    def __init__(self, message):
        parse_header = True
        for line in message.readlines():
            if parse_header:
                if self.header_break.match(line):
                    parse_header = False
                else:
                    item = self.header_item.match(line)
                    if item:
                        self.headers[item.groups()[0]] = item.groups()[1]