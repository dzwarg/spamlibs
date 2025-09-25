
# Python 3 Migration Plan

This document outlines the plan for migrating the spamlibs application from Python 2.7 to Python 3.

## Analysis

The first step is to analyze the project's dependencies and identify potential incompatibilities. The project uses the following major libraries:

*   Django
*   NLTK
*   NumPy

We need to check the Python 3 compatibility of the specific versions of these libraries used in the project.

## Migration Steps

1.  **Update `app.yaml`**: Change the runtime from `python27` to `python3`.
2.  **Update `main.py`**:
    *   The `main.py` file uses `webapp.util.run_wsgi_app`. This is not available in Python 3. We need to replace it with a WSGI-compliant server.
3.  **Update `urls.py`**:
    *   The `urls.py` file uses `django.conf.urls.defaults`. This is deprecated in newer versions of Django. We need to update it to `django.conf.urls`.
4.  **Update `spam/views.py`**:
    *   The `spam/views.py` file might contain Python 2 specific syntax. We need to run a tool like `2to3` to automatically convert the code to Python 3.
    *   We also need to check for any deprecated Django APIs used in this file.
5.  **Update `nltk`**:
    *   The `nltk` library is included in the project. We need to ensure that the version used is compatible with Python 3. If not, we need to upgrade it.
6.  **Update `requirements.txt`**:
    *   Create a `requirements.txt` file to list all the Python dependencies. This will make it easier to manage the dependencies in the future.
7.  **Testing**:
    *   After the migration, we need to thoroughly test the application to ensure that everything is working as expected.

## TODOs

*   [x] Update `app.yaml` to use `runtime: python3`.
*   [x] Update `main.py` to use a WSGI-compliant server.
*   [x] Update `urls.py` to use `django.conf.urls`.
*   [x] Run `2to3` on `spam/views.py` and other Python files.
*   [x] Check for deprecated Django APIs in `spam/views.py`.
*   [x] Check the Python 3 compatibility of the `nltk` library and upgrade if necessary.
*   [x] Create a `requirements.txt` file.
*   [x] Test the application thoroughly.
