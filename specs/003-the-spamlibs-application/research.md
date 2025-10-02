# Research: Webhook Endpoint for Incoming Email (Revised)

**Key Areas of Research (Revised)**:

1.  **Django Webhook Handling**: Best practices for creating a POST endpoint in Django to receive external data.
2.  **Robust JSON Payload Handling**: Given an unknown schema, focus on safely reading the raw request body and attempting JSON parsing. Emphasize error handling for malformed JSON.
3.  **Comprehensive Logging**: Strategies for logging *all* incoming webhook request content (headers, raw body) to meet FR-005 and FR-007, even if the payload is malformed or its structure is unknown.
4.  **Performance**: Techniques to ensure the endpoint can service 1 email message per second (FR-008), considering the overhead of logging raw, potentially large payloads.
5.  **Security (Authentication/Authorization)**: Given FR-006 (accept all requests regardless of authentication), research will focus on robust input validation and error handling to prevent abuse, rather than authentication mechanisms.

**Initial Findings/Considerations (Revised)**:

*   **Django Views**: A simple function-based view or a `django.views.View` subclass can handle the POST request.
*   **Raw Payload Access**: Django's `request.body` provides access to the raw request body. This should be logged directly.
*   **JSON Parsing (Attempted)**: After logging the raw body, attempt `json.loads()` within a `try-except` block. If parsing fails, log the error but still return 200 OK as per FR-003, unless a critical error prevents even that.
*   **Comprehensive Logging**: Configure Python's standard `logging` module to capture request metadata (headers, method, path) and the raw `request.body`. Consider using a custom logger or middleware for this.
*   **Performance**: Logging large raw payloads might impact performance. Evaluate asynchronous logging or offloading to a message queue if FR-008 becomes a bottleneck. Initial implementation will be synchronous.
*   **Error Handling**: Implement `try-except` blocks for all parsing and processing steps. Ensure that even malformed requests are logged and, if possible, still result in a 200 OK response as per FR-003/FR-007.