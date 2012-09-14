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
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.data import load
from random import random
from models import Email, Lib, UserSetting
from datetime import datetime
import logging, math, sys
from google.appengine.api.mail import InboundEmailMessage
from google.appengine.ext.db import BadKeyError
from google.appengine.api import users

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
            output += input[input_idx]
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
    limit = 10
    
    qry = Email.all().order('-date')
    recent_spams = qry.fetch(limit)
    
    count = qry.count(limit=limit+1)
    
    qry = Email.all().order('-views')
    viewed_spams = qry.fetch(limit)
    
    qry = Email.all().order('-rating')
    popular_spams = qry.fetch(limit)
    
    ctx = RequestContext(request, {
        'recent_spams':recent_spams,
        'viewed_spams':viewed_spams,
        'popular_spams':popular_spams,
        'more':count==limit+1
    })    
    
    return render_to_response('index.html', context_instance=ctx)


def _pager(current, total, per_page):
    """
    Generate a set of pager context variables for templates to
    render a nice pagination control.
    
    :param integer current: The current page.
    :param integer total: The total number of items.
    :param integer per_page: The number of items per page.
    :rtype: dict
    """
    maxpgs = 5
       
    lwrbound = 1
    if current > maxpgs:
        lwrbound = current - maxpgs
        
    uprbound = math.ceil(float(total) / per_page)
    if (total-(current * per_page))/per_page >= maxpgs:
        uprbound = current + maxpgs
        
    pager = {
        'pages':[],
        'less': lwrbound > 1,
        'more': total > uprbound * per_page 
    }

    for x in range(lwrbound, int(uprbound)+1):
        pager['pages'].append(x)
    
    return pager
    
def list(request, page):
    """
    List all the spams in the system, using a paging output.
    
    :param HttpRequest request: A web request.
    :param integer page: The page to view.
    :rtype: An HttpResponse object.
    """
    pagesize = 10
    maxfwd = pagesize * 5 + 1
    
    order = 'date'
    if 'order' in request.GET:
        tmpo = request.GET['order']
        if tmpo[0] == '-':
            tmpo = tmpo[1:]
        if tmpo in Email.properties():
            order = request.GET['order']
    
    page = int(page)
        
    qry = Email.all().order(order)
    nspams = qry.count(offset=(page-1)*pagesize, limit=maxfwd)
    spams = qry.fetch(pagesize, offset=(page-1)*pagesize)
    
    ctx = RequestContext(request, {
        'spams':spams,
        'count':maxfwd,
        'pager':_pager(page, (page-1)*pagesize + nspams, 10),
        'order':order,
        'page':page
    })
    
    return render_to_response('list.html', context_instance=ctx)
    
    
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
    
    email.views += 1
    email.put()
    
    tokens = word_tokenize(email.body)
    tags = pos_tag(tokens)
    body = _colorize_output(email.body, tags)
    
    ctx = RequestContext(request, {
        'title':email.title, 
        'body':body,
        'views':email.views,
        'rating':email.rating
    })
    
    return render_to_response('output_raw.html', context_instance=ctx)


def supply(request):
    """
    If the HTTP Verb is GET: Provide a form for adding a new spam email message.
    
    If the HTTP Verb is POST: Save and process a new email message, and view
    the resulting message.
    
    :param HttpRequest request: A web request.
    :rtype: An HttpResponse object.
    """
    user = users.get_current_user()
    
    if user is None:
        return redirect(users.create_login_url('/supply'))
        
    usetting = UserSetting.gql('WHERE userid = :1', user.user_id())
    if usetting.count() != 1 or not usetting.get().is_contrib:
        return HttpResponseForbidden('<h1>Authorization Required</h1>')
        
    if request.method == 'GET':
        ctx = RequestContext(request, {})
        return render_to_response('input_form.html', context_instance=ctx)
        
    title = request.POST['title']
    input = request.POST['input']
    date = datetime.now()
    
    email = Email(title=title, body=input, date=date, views=0, rating=0)
    email.put()

    _process_new(email)
    
    return redirect('/view/%s' % email.key())
    

def rate(request, key):
    """
    Rate a spam-libbed spam email.
    
    :param HttpRequest request: A web request.
    :param string key: The identifier for a specific email.
    :rtype: An HttpResponse object
    """
    try:
        email = Email.get(key)
    except BadKeyError:
        raise Http404
    
    email.rating += 1;
    email.put()
    
    return HttpResponse('OK')
    
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
        
    email.views += 1
    email.put()
        
    if request.method == 'GET':
        libs = Lib.all().filter('email =', email).order('position')
        ctx = RequestContext(request, {
            'title':email.title, 
            'key':key,
            'libs':libs
        })
        
        return render_to_response('seed_fields.html', context_instance=ctx)
        
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
        
    ctx = RequestContext(request, {
        'key':key, 
        'title':email.title,
        'body':newbody,
        'is_processed':True,
        'views':email.views
    })
    return render_to_response('output_raw.html', context_instance=ctx)
    
def incoming(request, email):
    """
    Accept a new email message directly via the AppEngine email facility. The
    entire email message is contained in the POST body of *email*.
    
    :param HttpRequest request: A web request.
    :param string email: An email address.
    :rtype: An HttpResponse object.
    """
    logging.info('Incoming email received.')
    
    try:
        msg = InboundEmailMessage(request.raw_post_data)
        
        usetting = UserSetting.gql('WHERE email = :1', msg.sender)
        if usetting.count() == 0:
            logging.warn('Received email from an unrecognized sender: ' + msg.sender)
            
            return render_to_response('msg_receipt.email', mimetype='text/plain')
            
        if not usetting.get().is_contrib:
            logging.warn('Received email from an unauthorized contributor: ' + msg.sender)
            
            return render_to_response('msg_receipt.email', mimetype='text/plain')
            
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
            logging.info('Compiled plain-text email: body length=%d' % len(content))
            
            newtitle = msg.subject.replace('\n','').replace('\r','')
            email = Email(title=newtitle, body=content, date=date, views=0, rating=0)
            email.put()
            
            logging.info('Processing new data for tokens & tags')
            
            _process_new(email)
            
    except Exception, ex:
        logging.error('Error processing new email. %s' % ex)
    
    return render_to_response('msg_receipt.email', mimetype='text/plain')