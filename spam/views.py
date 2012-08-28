"""
=====
Views
=====

Views are methods that accept HttpRequest objects, and return HttpResponse objects.

For more information about django views, see the django documentation:
`<https://docs.djangoproject.com/en/dev/topics/http/views/>`_

Each of the views here is mapped to one URL.
"""

from django.shortcuts import render_to_response, redirect
from django.http import Http404
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.data import load
from random import random
import sys
from models import Email, Lib
from datetime import datetime
import logging
from google.appengine.api.mail import InboundEmailMessage
from google.appengine.ext.db import BadKeyError

# load the tagset and help for individual terms
tagdict = load('help/tagsets/upenn_tagset.pickle')

# the probability of replacement, per-tag
repl_prop = {
    'NN': 0.25,
    'NNS': 0.25,
    'NNP': 0.35,
    'PRP': 0.15,
    'PRP$': 0.15, 
    'VB': 0.25,
    'VBD': 0.25,
    'VBP': 0.25,
    'VBZ': 0.25,
    'VBG': 0.25,
    'JJ': 0.5,
    'CD': 1.0
}

def _colorize_output(input, tags):
    """
    Generate a colorized output of the input, based on the tag types.
    
    :param string input: The input string
    :param list tags: The tags of the input string
    :rtype: An HTML string of colorized output.
    """
    output = ''
    input_idx = 0
    tag_idx = 0
    while tag_idx < len(tags):
        next_idx = input_idx + len(tags[tag_idx][0])
        try:
            tagtype = tags[tag_idx][1]
            tagdesc = tagdict[tagtype][0]
            tagdesc = tagdesc.replace('"','&quot;')
            text = input[input_idx:next_idx]
            output += '<span data-html="false" data-content="%s" data-placement="bottom" data-trigger="hover">%s</span>' % (tagdesc, text,)
        except KeyError as ke:
            output += input[input_idx:next_idx]
        tag_idx += 1
        input_idx = next_idx
        
        while input_idx < len(input) and (input[input_idx] == ' ' or input[input_idx] == '\r' or input[input_idx] == '\n'):
            if input[input_idx] == '\n':
                output += '<br/>'
            elif input[input_idx] == ' ':
                output += ' '

            input_idx += 1
    
    return output
    
    
def _generate_fields(email, input, tags):
    """
    Generate the terms to swap out, randomly.
    
    :param models.Email email: The input email message.
    :param string input: The input string.
    :param list tags: The tags of the input string.
    """
    input_idx = 0
    for tag in tags:
        if tag[1] in repl_prop and random() < repl_prop[tag[1]]:
            # make a field
            lib = Lib(email=email, original=tag[0], position=input_idx, description=tagdict[tag[1]][0])
            lib.put()
            
        input_idx = input_idx + len(tag[0])
        while input_idx < len(input) and (input[input_idx] == ' ' or input[input_idx] == '\r' or input[input_idx] == '\n'):
            input_idx += 1
            
            
def _process_new(email):
    """
    Process a new email, by tokenizing the incoming email message and generating
    the fields/terms to lib.
    
    :param models.Email email: The input email message.
    """
    tokens = word_tokenize(email.body)
    tags = pos_tag(tokens)
    _generate_fields(email, email.body, tags)
    
    
def index(request):
    """
    Generate the front page of spamlibs. This shows the 10 most recent spam
    email messages, and allows users to seed and view them.
    
    :param HttpRequest request: A web request.
    :rtype: An HttpResponse object.
    """
    spams = Email.all().fetch(10)
    return render_to_response('index.html', {'spams':spams})

    
def view(request, key):
    """
    View an original spam email message. The email message is specified by *key*.
    If the specified email cannot be found, this raises a 404 error.
    
    :param HttpRequest request: A web request.
    :param string key: The identifier for a specific email.
    :rtype: An HttpResponse object.
    """
    try:
        email = Email.get(key)
    except BadKeyError, ex:
        raise Http404
    
    tokens = word_tokenize(email.body)
    tags = pos_tag(tokens)
    body = _colorize_output(email.body, tags)
    
    return render_to_response('output_raw.html', {'title':email.title, 'body':body})


def supply(request):
    """
    If the HTTP Verb is GET: Provide a form for adding a new spam email message.
    
    If the HTTP Verb is POST: Save and process a new email message, and view
    the resulting message.
    
    :param HttpRequest request: A web request.
    :rtype: An HttpResponse object.
    """
    if request.method == 'GET':
        return render_to_response('input_form.html', {})
        
    title = request.POST['title']
    input = request.POST['input']
    date = datetime.now()
    
    email = Email(title=title, body=input, date=date)
    email.put()

    _process_new(email)
    
    return redirect('/view/%s' % email.key())
    
    
def seed(request, key):
    """
    Provide a form to seed, or populate, the libs for a specific spam email.
    The email message is specified by *key*. If the specified email cannot be 
    found, this raises a 404 error.    
    
    :param HttpRequest request: A web request.
    :param string key: The identifier for a specific email.
    :rtype: An HttpResponse object.
    """
    try:
        email = Email.get(key)
    except BadKeyError:
        raise Http404
        
    if request.method == 'GET':
        libs = Lib.all().filter('email =', email).order('position')
        return render_to_response('seed_fields.html', {'title':email.title, 'key':key, 'libs':libs})
        
    ls = []
    for l in request.POST.items():
        ls.append( (l[0], l[1], Lib.get(l[0]),) )
        
    ls.sort(cmp=lambda x,y: cmp(x[2].position, y[2].position))
        
    newbody = ''
    bodyidx = 0
    for l in ls:
        newbody += email.body[bodyidx:l[2].position]
        bodyidx = l[2].position
        
        newbody += l[1]
        bodyidx += len(l[2].original)
    
    newbody += email.body[bodyidx:]
        
    return render_to_response('output_raw.html', {'key':key, 'title':email.title, 'body':newbody, 'is_processed':True})
    
def incoming(request, email):
    """
    Accept a new email message directly via the AppEngine email facility. The
    entire email message is contained in the POST body of *email*.
    
    :param HttpRequest request: A web request.
    :param string email: An email address.
    :rtype: An HttpResponse object.
    """
    logging.info('Incoming email received.')
    
    msg = InboundEmailMessage(request.raw_post_data)
    
    content = ''
    for content_type, body in msg.bodies('text/plain'):
        headers = True
        date = False
        for line in str(body).split('\n'):
            if not date:
                parts = line.split(' ')
                line = ' '.join(parts[len(parts)-5:])
                date = datetime.strptime(line, '%a %b %d %H:%M:%S %Y')
                logging.debug(str(date))
                
            if headers and line == '':
                headers = False
            elif not headers:
                content += '%s\n' % line
                
    if content == '':
        logging.warn('Received an email, but no text/plain bodies.')
    else:
        email = Email(title=msg.subject, body=content, date=date)
        email.put()

        _process_new(email)
    
    return render_to_response('msg_receipt.email')