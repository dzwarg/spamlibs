# Quickstart: Data Extraction Script

This guide explains how to run the data extraction script and verify its output.

## Prerequisites
- Python 3
- `google-cloud-datastore` library installed (`pip install google-cloud-datastore`)
- Authenticated with gcloud (`gcloud auth application-default login`)

## Running the script
1. Save the script as `extract_data.py`.
2. Run the script from your terminal:
   ```bash
   python extract_data.py
   ```

## Verification
1. The script will create a file named `spamlibs_export.json` in the same directory.
2. The JSON file will contain a list of all `Email` and `Lib` entities from the Datastore.
3. If there is no data, the file will contain an empty list.
4. If there are errors (e.g., authentication), the script will print an error message to the console.
