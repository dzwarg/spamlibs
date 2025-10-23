# Tasks: Create a sample script for data extraction

**Input**: Design documents from `/specs/006-create-a-sample/`
**Prerequisites**: plan.md, research.md, data-model.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- The script will be created in a new `scripts/` directory at the root of the project.

## Phase 3.1: Setup
- [X] T001 Create a new directory `scripts/` at the project root.
- [X] T002 Create a new file `scripts/extract_data.py`.
- [X] T003 Create a new file `scripts/requirements.txt` and add `google-cloud-datastore` to it.
- [X] T004 Create a new directory `tests/scripts/`.
- [X] T005 Create a new file `tests/scripts/test_extract_data.py`.

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [X] T006 [P] In `tests/scripts/test_extract_data.py`, write a failing unit test for authenticating with Google Cloud Datastore.
- [X] T007 [P] In `tests/scripts/test_extract_data.py`, write a failing unit test for fetching data from Datastore.
- [X] T008 [P] In `tests/scripts/test_extract_data.py`, write a failing unit test for writing data to a JSON file.

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T009 In `scripts/extract_data.py`, implement the `authenticate` function to connect to Google Cloud Datastore using Application Default Credentials.
- [X] T010 In `scripts/extract_data.py`, implement the `fetch_data` function to retrieve all `Email` and `Lib` entities.
- [X] T011 In `scripts/extract_data.py`, implement the `write_to_json` function to save the extracted data to `spamlibs_export.json`.

## Phase 3.4: Integration
- [X] T012 In `scripts/extract_data.py`, implement the `main` function to orchestrate the script: authenticate, fetch data, and write to a file.

## Phase 3.5: Polish
- [X] T013 [P] Add logging to the script to provide feedback on the extraction process.
- [X] T014 [P] Add docstrings to all functions in the script.
- [X] T015 [P] Add error handling for potential issues like authentication failure or file write errors.

## Dependencies
- Setup (T001-T005) before everything.
- Tests (T006-T008) before implementation (T009-T011).
- T009 blocks T010.
- T010 blocks T011.
- Implementation before integration (T012).
- Integration before polish (T013-T015).

## Parallel Example
```
# Launch T006-T008 together:
Task: "In `tests/scripts/test_extract_data.py`, write a failing unit test for authenticating with Google Cloud Datastore."
Task: "In `tests/scripts/test_extract_data.py`, write a failing unit test for fetching data from Datastore."
Task: "In `tests/scripts/test_extract_data.py`, write a failing unit test for writing data to a JSON file."
```
