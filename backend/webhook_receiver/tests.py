import json
import logging
import os

from django.test import TestCase, Client
from django.urls import reverse

from .models import IncomingMessage

class WebhookReceiverViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('webhook_receiver')
        
        # Load the valid payload from the JSON file
        payload_path = os.path.join(os.path.dirname(__file__), 'valid_payload.json')
        with open(payload_path) as f:
            self.valid_payload = json.load(f)

    def test_post_request_with_valid_payload_returns_200_ok(self):
        response = self.client.post(self.url, json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(IncomingMessage.objects.exists())

    def test_get_request_returns_405_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_valid_json_payload_is_logged(self):
        with self.assertLogs('webhook_receiver.views', level='INFO') as cm:
            self.client.post(self.url, json.dumps(self.valid_payload), content_type='application/json')
            # Check for a substring of the large payload to avoid making the test too brittle
            self.assertIn('Parsed JSON Payload:', cm.output[3])

    def test_malformed_json_payload_returns_400_bad_request(self):
        malformed_payload = "{'sender': 'test@example.com'" # Invalid JSON
        with self.assertLogs('webhook_receiver.views', level='ERROR') as cm:
            response = self.client.post(self.url, malformed_payload, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Malformed JSON payload:", cm.output[0])

    def test_missing_subject_field_returns_400(self):
        payload = self.valid_payload.copy()
        del payload['subject']
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_from_field_returns_400(self):
        payload = self.valid_payload.copy()
        del payload['from']
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_text_field_returns_400(self):
        payload = self.valid_payload.copy()
        del payload['text']
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_format_is_handled_gracefully(self):
        payload = self.valid_payload.copy()
        payload['date'] = 'not a date'
        response = self.client.post(self.url, json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Verify that the message was created, but the date is None
        message = IncomingMessage.objects.latest('id')
        self.assertIsNone(message.date)