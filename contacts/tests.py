from django.test import TestCase

from contacts.forms import ContactForm
from contacts.models import Contact


# Create your tests here.

class ContactsTest(TestCase):

    def test_contact_is_valid(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "Ivanov",
                                               "phone_number": '0877317469',
                                               "email":"ivanivanov122201@gmail.com",
                                               "content":"#ffffff"})
        self.assertTrue(form.is_valid())

    def test_contact_form_is_valid_without_phone(self):
        form = ContactForm(data={"first_name": "Ivan",
                                 "last_name": "Ivanov",
                                 "email": "ivanivanov122201@gmail.com",
                                 "content": "#ffffff"})
        self.assertTrue(form.is_valid())

    def test_contact_form_is_not_valid_first_name(self):
        form = ContactForm(data={"first_name": "",
                                 "last_name": "Ivanov",
                                 "email": "ivanivanov122201@gmail.com",
                                 "content": "#ffffff"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['Please enter your name.'])

    def test_contact_form_is_not_valid_with_wrong_email(self):
        form = ContactForm(data={"first_name": "Ivan",
                                 "last_name": "Ivanov",
                                 "email": "ivanivanov122201",
                                 "content": "#ffffff"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Please enter a valid email address.'])

    def test_contact_form_is_not_valid_with_wrong_phone_number(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "Ivanov",
                                               "phone_number": '08773174693213123213',
                                               "email":"ivanivanov122201@gmail.com",
                                               "content":"#ffffff"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'], ['Please enter a valid phone number.'])

    def test_contact_form_is_not_valid_with_empty_content(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "Ivanov",
                                               "email":"ivanivanov122201@gmail.com",
                                               "content":""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'], ['Please enter your message.'])

    def test_contact_form_is_not_valid_with_empty_email(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "Ivanov",
                                               "email":"",
                                               "content":"123"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Please enter your email address.'])

    def test_contact_form_is_not_valid_with_first_name_too_long(self):
        form = ContactForm(data={"first_name": "Ivan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrIvan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrwerfdsfdsfdsIvan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrwerfdsfdsfdswerfdsfdsfds",
                                "last_name": "Ivanov",
                                               "email":"",
                                               "content":"123"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['Your name is too long.'])

    def test_contact_form_is_not_valid_with_last_name_too_long(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "Ivan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrIvan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrwerfdsfdsfdsIvan321321312321sdadsadsadsadsadsadsadsadsadsafsffdsferwerewrwerfdsfdsfdswerfdsfdsfds",
                                               "email":"",
                                               "content":"123"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], ['Your name is too long.'])

    def test_contact_form_is_not_valid_with_last_name_missing(self):
        form = ContactForm(data={"first_name": "Ivan",
                                "last_name": "",
                                               "email":"",
                                               "content":"123"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], ['Please enter your name.'])

