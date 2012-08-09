from django.shortcuts import render_to_response
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.data import load
from random import random
import sys

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
    
def form_output(tagdict, input, tags):
    output = ''
    input_idx = 0
    tag_idx = 0
    while tag_idx < len(tags):
        next_idx = input_idx + len(tags[tag_idx][0])
        if tags[tag_idx][1] in repl_prop and random() < repl_prop[tags[tag_idx][1]]:
            # form output
            output += '<input type="text" placeholder="%s" />' % (tagdict[tags[tag_idx][1]][0],)
        else:
            output += input[input_idx:next_idx]
            
        tag_idx += 1
        input_idx = next_idx
        
        while input_idx < len(input) and (input[input_idx] == ' ' or input[input_idx] == '\r' or input[input_idx] == '\n'):
            output += input[input_idx]
            input_idx += 1
    
    return output
    
def index(request):
    if request.method == 'GET':
        input = """My dear friend!
I read your ad in our Love Contact Agencies. My name is Sveta, and My age 28 year, my height is 170 cm. I graduated from Academy and am working as an agent. I'm interested in: gymnastics, skating and home-making. I'm independent, don't smoke or drink. I liked your photo and I want to know everything about you, write me. Go to my acc http://www.richardrobin.webpin.com Best wishes."""
    else:
        input = request.POST['input']
    tokens = word_tokenize(input)
    tags = pos_tag(tokens)
    pretty = colorize_output(tagdict, input, tags)
    form = form_output(tagdict, input, tags)
    
    return render_to_response('index.html', {
        'place': 'world',
        'input': input,
        'tagged': pretty,
        'form': form
    })
