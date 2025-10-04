# Implementation Plan: Revise URLs and Message Data Model

**Branch**: `004-revise-urls-to` | **Date**: 2025-10-02 | **Spec**: [link]
**Input**: Feature specification from `/specs/004-revise-urls-to/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

## Summary
The feature will revise the URL routing to serve the "hello world" message from the root URL '/' and establish a clear data model for incoming messages based on the provided "example-message.json" file.

## Technical Context
**Language/Version**: Python 3.11
**Primary Dependencies**: Django, NLTK
**Storage**: Google App Engine Datastore
**Testing**: pytest
**Target Platform**: Google App Engine
**Project Type**: web
**Performance Goals**: Not specified
**Constraints**: Must be compatible with Google App Engine Python 3.11 runtime.
**Scale/Scope**: Not specified

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Simplicity and Focus**: Yes, this simplifies the application's entry point and clarifies the data structure.
- **User-Centric Fun**: Neutral, this is a backend improvement.
- **Testability**: Yes, clear acceptance criteria are defined.
- **Clear and Maintainable Code**: Yes, this improves maintainability.
- **Convention over Configuration**: Yes, this uses Django's URL routing conventions.

## Project Structure

### Documentation (this feature)
```
specs/004-revise-urls-to/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)
```
backend/
├── manage.py
├── spamlibs_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hello_world/
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── webhook_receiver/
    ├── models.py
    ├── views.py
    └── urls.py
```

**Structure Decision**: Option 2: Web application

## Phase 0: Outline & Research
Completed in `research.md`.

## Phase 1: Design & Contracts
Completed in `data-model.md`, `contracts/webhook.yaml`, and `quickstart.md`.

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Create tasks to update the URL configuration to route '/' to the "hello world" view.
- Create tasks to define the `IncomingMessage` model based on `data-model.md`.
- Create tasks to implement validation for the `IncomingMessage` model.
- Create tasks to update the frontend to submit the form to the root URL (`/`) using `fetch`.
- Create a task to write an E2E test to verify the form submission.

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

## Frontend Changes
- The form in `backend/hello_world/templates/hello_world/index.html` already uses the `fetch` API to `POST` data to the backend.
- The `Content-Type` header is correctly set to `application/json`.
- The plan is to update the `fetch` call to POST to the root URL (`/`) instead of `/webhook/incoming`.

## Testing
- An E2E test will be created to verify the form submission.
- The test will:
    1. Navigate to the root URL (`/`).
    2. Fill in the message form.
    3. Click the submit button.
    4. Intercept the `fetch` request and assert that the request is a `POST` request to the correct URL (`/`) with the correct `Content-Type` header (`application/json`) and the correct payload.
    5. The existing E2E test `e2e_tests/test_hello_world.py` will be updated or a new one will be created.

## Complexity Tracking
None

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command)
- [x] Phase 4: Implementation complete
- [x] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented