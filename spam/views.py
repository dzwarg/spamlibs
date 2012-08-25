from django.shortcuts import render_to_response, redirect
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.data import load
from random import random
import sys
from models import Email, Lib, EmailRequest
from datetime import datetime
import logging
from google.appengine.api.mail import InboundEmailMessage

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

def colorize_output(tagdict, input, tags):
    """
    Colorize the output with HTML span elements.
    """
    output = ''
    input_idx = 0
    tag_idx = 0
    while tag_idx < len(tags):
        next_idx = input_idx + len(tags[tag_idx][0])
        try:
            output += '<span class="%s" title="%s">%s</span>' % (tags[tag_idx][1], tagdict[tags[tag_idx][1]][0], input[input_idx:next_idx],)
        except KeyError as ke:
            output += input[input_idx:next_idx]
        tag_idx += 1
        input_idx = next_idx
        
        while input_idx < len(input) and (input[input_idx] == ' ' or input[input_idx] == '\r' or input[input_idx] == '\n'):
            output += input[input_idx]
            input_idx += 1
    
    return output
    
    
def generate_fields(email, tagdict, input, tags):
    input_idx = 0
    for tag in tags:
        if tag[1] in repl_prop and random() < repl_prop[tag[1]]:
            # make a field
            lib = Lib(email=email, original=tag[0], position=input_idx, description=tagdict[tag[1]][0])
            lib.put()
            
        input_idx = input_idx + len(tag[0])
        while input_idx < len(input) and (input[input_idx] == ' ' or input[input_idx] == '\r' or input[input_idx] == '\n'):
            input_idx += 1
            
            
def process_new(email):
    tokens = word_tokenize(email.body)
    tags = pos_tag(tokens)
    form = generate_fields(email, tagdict, email.body, tags)
    
def index(request):
    spams = Email.all().fetch(10)
    return render_to_response('index.html', {'spams':spams})

    
def view(request, key):
    email = Email.get(key)
    
    tokens = word_tokenize(email.body)
    tags = pos_tag(tokens)
    body = colorize_output(tagdict, email.body, tags)
    
    return render_to_response('output_raw.html', {'title':email.title, 'body':body})


def supply(request):
    if request.method == 'GET':
        return render_to_response('input_form.html', {})
        
    title = request.POST['title']
    input = request.POST['input']
    date = datetime.now()
    
    email = Email(title=title, body=input, date=date)
    email.put()

    process_new(email)
    
    return redirect('/view/%s' % email.key())
    
    
def seed(request, key):
    email = Email.get(key)
    
    if request.method == 'GET':
        libs = Lib.all().filter('email =', email).order('position').fetch(10)
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
    logging.debug('Incoming email received.')
    
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
    
    email = Email(title=msg.subject, body=content, date=date)
    email.put()

    process_new(email)
    
    return render_to_response('msg_receipt.email')