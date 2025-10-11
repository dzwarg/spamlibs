# Tasks: Revise URLs and Message Data Model

**Input**: Design documents from `/specs/004-revise-urls-to/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Phase 3.1: Setup
*No setup tasks required for this feature.*

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T001 [P] Contract test for `GET /` in `backend/hello_world/tests.py`.
- [x] T002 [P] Contract test for `POST /webhook/` in `backend/webhook_receiver/tests.py`.
- [x] T003 [P] E2E test for form submission to `/` in `e2e_tests/test_form_submission.py`.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T004 Update `backend/spamlibs_project/urls.py` to route `/` to `hello_world.views.index`.
- [x] T005 Create `IncomingMessage` model in `backend/webhook_receiver/models.py`.
- [x] T006 Update `backend/webhook_receiver/views.py` to use the `IncomingMessage` model.

## Phase 3.4: Polish
- [x] T007 [P] Add unit tests for `IncomingMessage` model validation in `backend/webhook_receiver/tests.py`.

## Dependencies
- Tests (T001-T003) before implementation (T004-T008).
- T005 (model) must be completed before T006 (view) and T007 (validation tests).

## Parallel Example
```
# Launch T001-T003 together:
Task: "Contract test for GET / in backend/hello_world/tests.py"
Task: "Contract test for POST /webhook/ in backend/webhook_receiver/tests.py"
Task: "E2E test for form submission to / in e2e_tests/test_form_submission.py"
```