# Data Model for Index Page Migration

This document describes the data models that will be migrated from the Python 2.7 application to the Python 3 application.

## 1. Models to be Migrated

The following models will be migrated from `python27/spam/models.py` to `backend/spam/models.py`:

*   **Email**: Represents a spam email.
    *   `title`: `CharField`
    *   `body`: `TextField`
    *   `date`: `DateTimeField`
    *   `rating`: `IntegerField`
    *   `views`: `IntegerField`
*   **Lib**: Represents a word to be replaced in the Mad Lib.
    *   `email`: `ForeignKey` to `Email`
    *   `part_of_speech`: `CharField`
    *   `position`: `IntegerField`
    *   `description`: `CharField`

## 2. Database Schema

The database schema for these models will be created using Django's migration framework. The existing data will be migrated using a separate data migration script.
