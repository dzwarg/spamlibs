import json
import logging
from google.cloud import datastore
from google.api_core import exceptions

logging.basicConfig(level=logging.INFO)

def authenticate():
    """Connect to Google Cloud Datastore using Application Default Credentials."""
    try:
        return datastore.Client()
    except exceptions.DefaultCredentialsError as e:
        logging.error("Authentication failed. Please configure your Google Cloud credentials.")
        logging.error(e)
        return None

def fetch_data(client, kind):
    """Fetch all entities of a given kind from Datastore."""
    if not client:
        return []
    try:
        query = client.query(kind=kind)
        return list(query.fetch())
    except exceptions.GoogleAPICallError as e:
        logging.error(f"Error fetching data for kind {kind}: {e}")
        return []

def write_to_json(entities, filename):
    """Write a list of entities to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(entities, f, indent=2)
    except IOError as e:
        logging.error(f"Error writing to file {filename}: {e}")

def main():
    """Extract all Email and Lib entities and write them to a JSON file."""
    client = authenticate()
    if not client:
        return

    logging.info("Extracting Email entities...")
    emails = fetch_data(client, "Email")
    logging.info(f"Found {len(emails)} Email entities.")

    logging.info("Extracting Lib entities...")
    libs = fetch_data(client, "Lib")
    logging.info(f"Found {len(libs)} Lib entities.")

    email_list = []
    for email in emails:
        email_dict = dict(email)
        email_dict['id'] = email.key.id_or_name
        if 'date' in email_dict and hasattr(email_dict['date'], 'isoformat'):
            email_dict['date'] = email_dict['date'].isoformat()
        email_list.append(email_dict)

    lib_list = []
    for lib in libs:
        lib_dict = dict(lib)
        if 'email' in lib and lib['email']:
            lib_dict['email'] = lib['email'].id_or_name
        lib_list.append(lib_dict)

    data = {
        "emails": email_list,
        "libs": lib_list,
    }

    write_to_json(data, "spamlibs_export.json")
    logging.info("Data extraction complete. See spamlibs_export.json")

if __name__ == '__main__':
    main()