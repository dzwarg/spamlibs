# Quickstart: Webhook Endpoint for Incoming Email

To test the webhook endpoint, you can send a POST request with a JSON payload representing an incoming email.

## Example using `curl`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "test@example.com",
    "recipient": "spamlibs@your-app.appspot.com",
    "subject": "Test Spam Email",
    "body_plain": "This is a test email body."
  }' \
  https://your-app.appspot.com/incoming
```

**Note**: Replace `https://your-app.appspot.com/incoming` with the actual URL of your deployed webhook endpoint.

