from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class HomePageTest(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('common:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('common:home'))
        self.assertTemplateUsed(response, 'common/landing_page.html')