from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class TestDashboardView(TestCase):
    def setUp(self):
        self.user_credentials = {
            "username": "test",
            "email": "test@test.com",
            "password": "12test34",
        }

        self.user = UserModel.objects.create_user(
            **self.user_credentials
        )

        self.url = reverse('dashboard')

    def test_redirect_if_user_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_dashboard_view_renders_for_logged_in_user(self):
        self.client.login(
            email=self.user_credentials['email'],
            password=self.user_credentials['password'],
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        self.assertIn('result', response.context)
        self.assertIn('data_labels', response.context)
        self.assertIn('data_values', response.context)
        self.assertIn('attribute_descriptions', response.context)

        self.assertEqual(
            response.context['data_labels'],
            ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
        )
