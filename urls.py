"""
====
URLs
====

File: urls.py

URL mappings for the endpoints available for Spamlibs. There are only five 
endpoints:

* ``/``: The front page.
* ``/view/<key>``: View the original spam message.
* ``/seed/<key>``: Seed and view a seeded spam message.
* ``/supply``: Input a new spam email into the application.
* ``/_ah/mail/<email>``: An AppEngine URL to receive spam email directly.
"""
from django.conf.urls.defaults import *
from spam import views

urlpatterns = patterns('',
    # The main page/index view
    (r'^$', views.index),
    
    # A list of all spams
    (r'^list/(?P<page>\d*)$', views.list),
    
    # View a specific spam
    (r'^view/(?P<key>.*)$', views.view),
    
    # Generate forms for all the fields in a spam
    (r'^seed/(?P<key>.*)$', views.seed),
    
    # Input an email from an HTML form
    (r'^supply$', views.supply),
    
    # Rate a spamlibbed email
    (r'^rate/(?P<key>.*)$', views.rate),
    
    # Input an email from an email submission
    (r'^_ah/mail/(?P<email>.*)$', views.incoming),
)
