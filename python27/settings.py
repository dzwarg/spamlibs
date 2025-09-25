"""
========
Settings
========

File: settings.py

Application settings specific to this running version of spamlibs. More 
documentation on the settings module can be found in the django documentation.

.. data:: DEBUG

   Set the application to run in debug mode and print verbose error messages. 
   
.. data:: TEMPLATE_DEBUG

   Set the application to run templates in debug mode, and print verbose error messages.

.. data:: ROOT_URLCONF

   The name of the module that contains the url mappings.
   
.. data:: MIDDLEWARE_CLASSES

   The set of django middleware classes.
   
.. data:: ROOT_PATH

   The absolute filesystem path to the root of the django project.
   
.. data:: TEMPLATE_DIRS

   The directories that contain the web templates
"""
import os

#: Set the application to run in debug mode and print verbose error messages.
DEBUG=False

#: Set the application to run templates in debug mode, and print verbose error messages.
TEMPLATE_DEBUG=DEBUG

#: The name of the module that contains the URL mappings.
ROOT_URLCONF = 'urls'

#: The set of middleware classes.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'spam.context_processors.user',
)

#: The root filesystem path, absolute.
ROOT_PATH = os.path.dirname(__file__)

#: The directories that contain templates.
TEMPLATE_DIRS = (
    ROOT_PATH + '/templates',
)