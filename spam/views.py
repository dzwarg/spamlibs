from django.shortcuts import render_to_response, redirect
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.data import load
from random import random
import sys
from models import Email, Lib
from datetime import datetime

# load the tagset and help
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
    output = ''
    input_idx = 0
    tag_idx = 0
    while tag_idx < len(tags):
        next_idx = input_idx + len(tags[tag_idx][0])
        output += '<span class="%s" title="%s">%s</span>' % (tags[tag_idx][1], tagdict[tags[tag_idx][1]][0], input[input_idx:next_idx],)
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
    
def index(request):
    spams = Email.all().fetch(10)
    return render_to_response('index.html', {'spams':spams})

"""
    if request.method == 'GET':
        input = " " "My dear friend!
I read your ad in our Love Contact Agencies. My name is Sveta, and My age 28 year, my height is 170 cm. I graduated from Academy and am working as an agent. I'm interested in: gymnastics, skating and home-making. I'm independent, don't smoke or drink. I liked your photo and I want to know everything about you, write me. Go to my acc http://www.richardrobin.webpin.com Best wishes." " "
    else:
        input = request.POST['input']
        email = Email(title='Test', body=input)
        email.put()
    
    return render_to_response('index.html', {
        'place': 'world',
        'input': input,
        'tagged': pretty,
        'form': form
    })
"""
    
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

    tokens = word_tokenize(input)
    tags = pos_tag(tokens)
    form = generate_fields(email, tagdict, input, tags)
    
    return redirect('/view/%s' % email.key())
    
def seed(request, key):
    email = Email.get(key)
    libs = Lib.all().filter('email =', email).fetch(10)
    
    return render_to_response('seed_fields.html', {'title':email.title, 'libs':libs})