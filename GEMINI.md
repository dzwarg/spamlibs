# Project Overview

This is a Google App Engine web application that turns spam emails into Mad Libs. It is written in Python and uses the Django web framework and the Natural Language Toolkit (NLTK).

The application works by receiving spam emails, identifying parts of speech (nouns, verbs, adjectives, etc.) in the email text using NLTK, and then replacing them with words provided by the user to create a humorous result.

## Building and Running

This is a Google App Engine project and can be run using the App Engine SDK.

**To run the application locally:**

```bash
python backend/manage.py runserver
```

**To deploy the application:**

```bash
scripts/deploy.sh
```

## Testing

To run all tests, use the following script:

```bash
scripts/run_tests.sh
```

This will execute both the Django unit tests and the Playwright E2E tests and provide a summary of the results.
## Development Conventions

*   The project follows the standard Django project structure.
*   The application uses the NLTK library for natural language processing.
*   The application uses the Google App Engine datastore for data persistence.
*   The frontend is built with Django templates and Bootstrap.

### Commit Messages

Commit messages should follow the Conventional Commits specification. Each commit message should be structured as follows:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Example:**

```
feat(spec-001): Implement 'hello world' and restructure project

This commit marks the beginning of spec-driven development for this project.

It introduces the initial implementation of the "Display a 'hello world' page to users" feature, as defined in spec-001.

Changes include:
- A new Django project in the backend directory.
- A hello_world app with a view, template, and URL configuration.
- A test to verify the feature.
- Feature specification and implementation plan in the specs directory.
- The .specify directory and its contents for the new workflow.
- The original project files have been moved into the python27 directory to preserve them for future migration.
```
