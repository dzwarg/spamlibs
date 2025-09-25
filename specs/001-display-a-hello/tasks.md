# Tasks: Display a "hello world" page to users.

**Input**: Design documents from `/Users/dzwarg/code/spamlibs/specs/001-display-a-hello/`
**Prerequisites**: plan.md (required), research.md, data-model.md, quickstart.md

## Phase 3.1: Setup
- [X] T001 Create a new Django app named `hello_world`.
- [X] T006 Add 'hello_world' to INSTALLED_APPS in backend/spamlibs_project/settings.py.

## Phase 3.2: Core Implementation
- [X] T002 Create a view in `hello_world/views.py` that renders a template.
- [X] T003 Create a template in `hello_world/templates/hello_world/index.html` that displays "hello world".
- [X] T004 Create a `hello_world/urls.py` and include it in the main `urls.py`.

## Phase 3.3: Tests
- [X] T005 Write a test in `hello_world/tests.py` to verify that the main page returns a 200 status code and contains the text "hello world".

## Dependencies
- T001 must be completed before T002, T003, T004, and T005.
- T002 and T003 must be completed before T004.
- T004 must be completed before T005.
- T006 must be completed before running the application.