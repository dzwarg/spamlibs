# Data Model: IncomingMessage

## Entity: IncomingMessage

Represents an email message received by the application.

### Fields
- **attachments**: A list of attached files.
- **headers**: A dictionary of email headers.
- **headerLines**: An array of objects, each with `key` and `line` properties.
- **html**: The HTML body of the email.
- **text**: The plain text body of the email.
- **textAsHtml**: The plain text body of the email as HTML.
- **subject**: The subject of the email.
- **date**: The date of the email.
- **to**: An object with `value`, `html`, and `text` properties.
- **from**: An object with `value`, `html`, and `text` properties.
- **messageId**: The message ID of the email.
- **raw**: The raw email content.
- **dkim**: An object with DKIM information.
- **spf**: An object with SPF information.
- **arc**: An object with ARC information.
- **dmarc**: An object with DMARC information.
- **bimi**: An object with BIMI information.
- **recipients**: An array of recipient email addresses.
- **session**: An object with session information.