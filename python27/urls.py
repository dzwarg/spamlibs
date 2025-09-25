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
from django.urls import re_path
from spam import views

urlpatterns = [
    # The main page/index view
    re_path(r'^$', views.index),
    
    # A list of all spams
    re_path(r'^list/(?P<page>\d*)$', views.list),
    
    # View a specific spam
    re_path(r'^view/(?P<key>.*)$', views.view),
    
    # Generate forms for all the fields in a spam
    re_path(r'^seed/(?P<key>.*)$', views.seed),
    
    # Input an email from an HTML form
    re_path(r'^supply$', views.supply),
    
    # Rate a spamlibbed email
    re_path(r'^rate/(?P<key>.*)$', views.rate),
    
    # Input an email from an email submission
    re_path(r'^_ah/mail/garbage@spamlibs.appspotmail.com$', views.incoming),
]