#!/bin/bash

# Run Django unit tests
echo "Running Django unit tests..."
python backend/manage.py test spam
spam_unit_result=$?

python backend/manage.py test webhook_receiver
webhook_receiver_unit_result=$?

# Start the local development server in the background
echo "Starting local development server..."
python backend/manage.py runserver > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for the server to be ready
sleep 10

# Run Playwright E2E tests
echo "Running Playwright E2E tests..."
python e2e_tests/test_spam.py
spam_e2e_result=$?

# Stop the local development server
echo "Stopping local development server..."
kill $SERVER_PID

# Summarize the results
echo "--------------------"
echo "Test Results Summary"
echo "--------------------"

if [ $spam_unit_result -eq 0 ]; then
    echo "✅ Django unit tests (spam): PASSED"
else
    echo "❌ Django unit tests (spam): FAILED"
fi

if [ $webhook_receiver_unit_result -eq 0 ]; then
    echo "✅ Django unit tests (webhook_receiver): PASSED"
else
    echo "❌ Django unit tests (webhook_receiver): FAILED"
fi

if [ $spam_e2e_result -eq 0 ]; then
    echo "✅ E2E test (spam): PASSED"
else
    echo "❌ E2E test (spam): FAILED"
fi

# Exit with a non-zero status code if any test failed
if [ $spam_unit_result -ne 0 ] || [ $webhook_receiver_unit_result -ne 0 ] || [ $spam_e2e_result -ne 0 ]; then
    exit 1
fi