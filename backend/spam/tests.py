from django.test import TestCase
from django.urls import reverse
from .models import Email, Lib
from datetime import datetime

class IndexViewTests(TestCase):
    def setUp(self):
        # Create some test data
        for i in range(15):
            Email.objects.create(
                title=f'Test Email {i}',
                body='This is a test email.',
                date=datetime.now(),
                rating=i,
                views=i * 10
            )

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_context(self):
        response = self.client.get(reverse('index'))
        self.assertTrue('recent_spams' in response.context)
        self.assertTrue('viewed_spams' in response.context)
        self.assertTrue('popular_spams' in response.context)
        self.assertTrue('more' in response.context)

        self.assertEqual(len(response.context['recent_spams']), 10)
        self.assertEqual(len(response.context['viewed_spams']), 10)
        self.assertEqual(len(response.context['popular_spams']), 10)
        self.assertTrue(response.context['more'])

class SpamModelTests(TestCase):
    def test_create_email(self):
        email = Email.objects.create(
            title='Test Email',
            body='This is a test email.',
            date=datetime.now(),
            rating=5,
            views=100
        )
        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(email.title, 'Test Email')

    def test_create_lib(self):
        email = Email.objects.create(
            title='Test Email',
            body='This is a test email.',
            date=datetime.now(),
            rating=5,
            views=100
        )
        lib = Lib.objects.create(
            email=email,
            original='test',
            position=10,
            description='A test word'
        )
        self.assertEqual(Lib.objects.count(), 1)
        self.assertEqual(lib.email, email)
