# Research: Data Extraction Script

## Decision
We will use the `google-cloud-datastore` library to connect to the Google Cloud Datastore and extract the data.

## Rationale
This is the official Google Cloud library for interacting with the Datastore from Python. It provides a straightforward API for querying and retrieving entities.

## Alternatives considered
- Using the Google Cloud API directly: This would be more complex and require more boilerplate code.
