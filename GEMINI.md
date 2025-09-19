# Project Overview

This is a Google App Engine web application that turns spam emails into Mad Libs. It is written in Python and uses the Django web framework and the Natural Language Toolkit (NLTK).

The application works by receiving spam emails, identifying parts of speech (nouns, verbs, adjectives, etc.) in the email text using NLTK, and then replacing them with words provided by the user to create a humorous result.

## Building and Running

This is a Google App Engine project and can be run using the App Engine SDK.

**To run the application locally:**

```bash
dev_appserver.py .
```

**To deploy the application:**

```bash
appcfg.py update .
```

*TODO: The above commands are inferred from the project type. Verify that they are correct and update this section if necessary.*

## Development Conventions

*   The project follows the standard Django project structure.
*   The application uses the NLTK library for natural language processing.
*   The application uses the Google App Engine datastore for data persistence.
*   The frontend is built with Django templates and Bootstrap.
