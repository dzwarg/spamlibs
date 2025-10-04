#!/bin/bash

echo "Running Django unit tests..."
python backend/manage.py test hello_world
hello_world_unit_result=$?

python backend/manage.py test webhook_receiver
webhook_receiver_unit_result=$?

echo "Starting local development server..."
python backend/manage.py runserver > gunicorn.log &
server_pid=$!

# Wait for the server to start
sleep 5

echo "Running Playwright E2E tests..."
python e2e_tests/test_hello_world.py
hello_world_e2e_result=$?

python e2e_tests/test_form_submission.py
form_submission_e2e_result=$?

echo "Stopping local development server..."
kill $server_pid

echo "--------------------"
echo "Test Results Summary"
echo "--------------------"

if [ $hello_world_unit_result -eq 0 ]; then
    echo "✅ Django unit tests (hello_world): PASSED"
else
    echo "❌ Django unit tests (hello_world): FAILED"
fi

if [ $webhook_receiver_unit_result -eq 0 ]; then
    echo "✅ Django unit tests (webhook_receiver): PASSED"
else
    echo "❌ Django unit tests (webhook_receiver): FAILED"
fi

if [ $hello_world_e2e_result -eq 0 ]; then
    echo "✅ E2E test (hello_world): PASSED"
else
    echo "❌ E2E test (hello_world): FAILED"
fi

if [ $form_submission_e2e_result -eq 0 ]; then
    echo "✅ E2E test (form_submission): PASSED"
else
    echo "❌ E2E test (form_submission): FAILED"
fi

if [ $hello_world_unit_result -ne 0 ] || [ $webhook_receiver_unit_result -ne 0 ] || [ $hello_world_e2e_result -ne 0 ] || [ $form_submission_e2e_result -ne 0 ]; then
    exit 1
fi

exit 0