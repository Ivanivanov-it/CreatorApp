from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cards.choices import BorderStyleChoices
from cards.models import Card
# Create your tests here.




class CardModelTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.TestUser = UserModel.objects.create_user(username='testuser', password='testpassword123')
        self.TestCard = Card.objects.create(name="TestCard",
                                       border_color="#000000",
                                       border_style=BorderStyleChoices.SOLID,
                                       background_color="#ffffff",
                                       image_border_color="#ffffff",
                                       image_border_style=BorderStyleChoices.SOLID,
                                       accent_color="#ffffff",
                                       is_default=False,
                                       creator=self.TestUser)


    def test_card_border_style_is_correct(self):
        self.assertEqual(self.TestCard.border_style, "solid")

    def test_card_name_cannot_be_empty(self):
        TestCard = Card.objects.create(name="",
                                       border_color="#000000",
                                       border_style=BorderStyleChoices.SOLID,
                                       background_color="#ffffff",
                                       image_border_color="#ffffff",
                                       image_border_style=BorderStyleChoices.SOLID,
                                       accent_color="#ffffff",
                                       is_default=False,
                                       creator=self.TestUser)

        with self.assertRaises(ValidationError):
            TestCard.full_clean()

class CardViewTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.TestUser = UserModel.objects.create_user(username='testuser', password='testpassword123')
        self.TestCard = Card.objects.create(name="TestCard",
                                            border_color="#000000",
                                            border_style=BorderStyleChoices.SOLID,
                                            background_color="#ffffff",
                                            image_border_color="#ffffff",
                                            image_border_style=BorderStyleChoices.SOLID,
                                            accent_color="#ffffff",
                                            is_default=False,
                                            creator=self.TestUser)
        self.TestUser2 = UserModel.objects.create_user(username='testuser2', password='testpassword123')
        self.moderator = UserModel.objects.create_user(username='moderator', password='testpassword123')
        self.moderators_group = Group.objects.filter(name='Moderators').first()
        self.moderator.groups.add(self.moderators_group)



    def test_redirect_edit_if_not_logged_in(self):
        url = reverse('cards:edit_card', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,f"/no-permission/")

    def test_redirect_edit_if_logged_in_but_not_creator(self):
        self.client.login(username='testuser2', password='testpassword123')

        url = reverse('cards:edit_card', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/no-permission/")

    def test__edit_if_logged_in_and_creator(self):
        self.client.login(username='testuser', password='testpassword123')

        url = reverse('cards:edit_card', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'cards/edit_card.html')

    def test__edit_if_logged_in_and_not_creator_but_moderator(self):
        self.client.login(username='moderator', password='testpassword123')
        url = reverse('cards:edit_card', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'cards/edit_card.html')

    def test_redirect_delete_if_not_logged_in(self):
        url = reverse('cards:card_delete', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/no-permission/")

    def test_redirect_delete_if_logged_in_but_not_creator(self):
        self.client.login(username='testuser2', password='testpassword123')

        url = reverse('cards:card_delete', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/no-permission/")

    def test_delete_if_logged_in_and_creator(self):
        self.client.login(username='testuser', password='testpassword123')

        url = reverse('cards:card_delete', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/delete_confirm.html')

    def test_delete_if_logged_in_and_not_creator_but_moderator(self):
        self.client.login(username='moderator', password='testpassword123')
        url = reverse('cards:card_delete', kwargs={'pk': self.TestCard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/delete_confirm.html')
