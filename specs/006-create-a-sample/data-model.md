# Data Model: Spamlibs

The data for this feature is stored in Google Cloud Datastore and consists of two main entities:

## Email
Represents a single spam email.

**Fields**:
- `title` (String): The subject of the email.
- `body` (Text): The content of the email.
- `date` (DateTime): The date the email was received.
- `rating` (Integer): A user-assigned rating.
- `views` (Integer): The number of times the email has been viewed.

## Lib
A single word or phrase within an email that has been identified as a part of speech.

**Fields**:
- `email` (ForeignKey to Email): The email this lib belongs to.
- `original` (String): The original word or phrase.
- `position` (Integer): The position of the word in the email body.
- `description` (String): The part of speech (e.g., "noun", "verb").
