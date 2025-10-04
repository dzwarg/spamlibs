# Data Model: Incoming Webhook Payload (Unknown Structure)

Represents the raw, unvalidated data received from the webhook. The exact structure is unknown and will be logged as-is for later analysis and schema discovery.

**Attributes**:

*   `raw_payload` (string/object): The entire incoming request body, to be logged without prior validation or parsing into a specific schema.
*   `headers` (object): All incoming HTTP headers.
*   `method` (string): The HTTP method used (e.g., POST).
*   `path` (string): The request path.

**Example Raw Payload (for logging purposes)**:

```json
{
  "received_at": "2025-09-24T12:34:56Z",
  "method": "POST",
  "path": "/incoming",
  "headers": {
    "Content-Type": "application/json",
    "User-Agent": "ExampleWebhookSender/1.0"
  },
  "body": "{\"some_key\": \"some_value\", \"email_content\": \"...\"}"
}
```