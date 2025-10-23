#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "Deploying to Google App Engine..."
gcloud app deploy backend/app.yaml --project=spamlibs

echo "Running Playwright tests..."
python e2e_tests/test_spam.py

echo "Playwright test report generated. Open playwright-report/index.html in your browser to view it."
