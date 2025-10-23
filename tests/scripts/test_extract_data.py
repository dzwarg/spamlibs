import unittest
import json
from unittest.mock import patch, mock_open

from scripts import extract_data

class TestExtractData(unittest.TestCase):

    @patch('google.cloud.datastore.Client')
    def test_authenticate(self, mock_client):
        """Test that the authenticate function returns a datastore client."""
        client = extract_data.authenticate()
        mock_client.assert_called_once()
        self.assertEqual(client, mock_client.return_value)

    @patch('google.cloud.datastore.Client')
    def test_fetch_data(self, mock_client):
        """Test that fetch_data returns a list of entities."""
        mock_query = mock_client.query.return_value
        mock_query.fetch.return_value = [
            {'title': 'test1', 'body': 'body1'},
            {'title': 'test2', 'body': 'body2'},
        ]
        entities = extract_data.fetch_data(mock_client, 'TestKind')
        self.assertEqual(len(entities), 2)

    @patch('json.dump')
    def test_write_to_json(self, mock_json_dump):
        """Test that write_to_json writes data to a file."""
        mock_data = [{'key': 'value'}]
        with patch('builtins.open', mock_open()) as mock_file:
            extract_data.write_to_json(mock_data, 'test.json')
            mock_file.assert_called_with('test.json', 'w')
            mock_json_dump.assert_called_once_with(mock_data, mock_file(), indent=2)

if __name__ == '__main__':
    unittest.main()