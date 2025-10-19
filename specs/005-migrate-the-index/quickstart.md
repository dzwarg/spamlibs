# Quickstart for Index Page Migration

This document provides a quickstart guide for testing the migrated index page.

## 1. Prerequisites

*   Python 3.x
*   Django
*   gunicorn

## 2. Running the Application

1.  Start the development server:
    ```bash
    python backend/manage.py runserver
    ```
2.  Open a web browser and navigate to `http://127.0.0.1:8000/`.

## 3. Testing

1.  Verify that the index page loads and displays the same content as the old Python 2.7 application.
2.  Verify that the spam submission form is present and functional.
3.  Verify that the list of recent spam emails is displayed.
