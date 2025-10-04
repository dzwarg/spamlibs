# Tasks: The spamlibs application should provide an endpoint that can serve webhook requests.

**Input**: Design documents from `/Users/dzwarg/code/spamlibs/specs/003-the-spamlibs-application/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/webhook.yaml, quickstart.md

## Phase 3.1: Setup
- [X] T001 Create a new Django app named `webhook_receiver` in the `backend` directory.
- [X] T006 Add 'webhook_receiver' to INSTALLED_APPS in backend/spamlibs_project/settings.py.

## Phase 3.2: Core Implementation
- [X] T002 Implement the webhook view in `backend/webhook_receiver/views.py` to:
    - Safely read the raw request body.
    - Log all incoming content (headers, raw body).
    - Attempt JSON parsing (logging errors if malformed).
    - Return a 200 OK response.
- [X] T003 Define URL routing for the `/incoming` endpoint in `backend/webhook_receiver/urls.py` and include it in the main `backend/spamlibs_project/urls.py`.
- [X] T008 Modify `backend/hello_world/templates/hello_world/index.html` to include an HTML form that POSTs to `/webhook/incoming`.

## Phase 3.3: Tests
- [X] T004 Write unit tests in `backend/webhook_receiver/tests.py` for the webhook view, focusing on:
    - Logging behavior for valid and malformed JSON payloads.
    - Returning 200 OK for all requests.
    - Correctly parsing valid JSON (if applicable).
- [X] T005 Write an integration test using `curl` (as described in `quickstart.md`) to verify the endpoint's behavior.

## Phase 3.4: Redeploy
- [X] T007 Redeploy the application using `scripts/deploy.sh`.

## Dependencies
- T001 must be completed before T002 and T003.
- T006 must be completed before T002 and T003.
- T002 and T003 must be completed before T004.
- T008 must be completed before T005.
- T004 must be completed before T007.
- T007 must be completed before T005.