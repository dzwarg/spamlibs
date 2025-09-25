from django.test import TestCase

class HelloWorldViewTests(TestCase):
    def test_hello_world_view(self):
        response = self.client.get('/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello world")
