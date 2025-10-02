import json
import logging

from django.test import TestCase, Client
from django.urls import reverse

from .views import webhook_receiver

class WebhookReceiverViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('incoming_webhook') # Assuming 'incoming_webhook' is the name of the URL pattern

    def test_post_request_returns_200_ok(self):
        response = self.client.post(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_request_returns_405_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_valid_json_payload_is_logged(self):
        payload = {'sender': 'test@example.com', 'subject': 'Test Subject'}
        with self.assertLogs('webhook_receiver.views', level='INFO') as cm:
            self.client.post(self.url, json.dumps(payload), content_type='application/json')
            self.assertIn(f"Parsed JSON Payload: {payload}", cm.output[3]) # Corrected index

    def test_malformed_json_payload_is_logged_and_returns_200_ok(self):
        malformed_payload = "{'sender': 'test@example.com'" # Invalid JSON
        with self.assertLogs('webhook_receiver.views', level='ERROR') as cm:
            response = self.client.post(self.url, malformed_payload, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn("Malformed JSON payload:", cm.output[0])
