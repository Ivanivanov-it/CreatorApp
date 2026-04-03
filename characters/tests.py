from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from characters.forms import CharacterForm
from common.choices import CharacterType
from common.models import Role
from unittest.mock import patch, MagicMock


# Create your tests here.

JPEG_HEADER = b'\xff\xd8\xff' + b'\x00' * 100
PNG_HEADER  = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
WEBP_HEADER = b'RIFF' + b'\x00' * 4 + b'WEBP' + b'\x00' * 100
FAKE_BYTES  = b'this is not an image at all'


@override_settings(SECURE_SSL_REDIRECT=False)
class CharacterFormTest(TestCase):

    def setUp(self):
        UserModel = get_user_model()
        self.TestUser = UserModel.objects.create_user(username='testuser', password='testpassword123')

        self.role = Role.objects.filter(role='ATTACK')

    def test_form_valid_with_valid_data(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_when_roles_missing(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': "",
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn('roles', form.errors)

    def test_form_invalid_when_type_missing(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': "",
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)

    def test_form_invalid_when_stat_sum_above_100(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 33,
            'defense': 33,
            'hp': 55
        })

        self.assertFalse(form.is_valid())
        self.assertIn("The total number of stats must not exceed 100",form.errors['__all__'])

    def test_form_invalid_when_attack_below_1(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 0,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Ensure this value is greater than or equal to 1.", form.errors['attack'])

    def test_form_invalid_when_no_attack(self):
        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn("attack",form.errors)

    def test_form_valid_with_jpeg_image(self):
        file = SimpleUploadedFile('photo.jpg', JPEG_HEADER, content_type='image/jpeg')


        with patch('cloudinary.uploader.upload_image', return_value='fake/photo'):
            with patch('cloudinary.forms.CloudinaryFileField.to_python', return_value='fake/photo'):
                form = CharacterForm(
                    data={
                        'name': 'Ivan',
                        'title': 'Ivanov',
                        'type': CharacterType.OTHER,
                        'description': "123",
                        'roles': self.role,
                        'creator': self.TestUser,
                        'attack': 3,
                        'defense': 3,
                        'hp': 3,
                    },
                    files={
                        'image_url': file
                    }
                )
                self.assertTrue(form.is_valid())

    def test_form_valid_with_png_image(self):
        file = SimpleUploadedFile('photo.png', PNG_HEADER, content_type='image/png')

        with patch('cloudinary.uploader.upload_image', return_value='fake/photo'):
            with patch('cloudinary.forms.CloudinaryFileField.to_python', return_value='fake/photo'):
                form = CharacterForm(
                    data={
                        'name': 'Ivan',
                        'title': 'Ivanov',
                        'type': CharacterType.OTHER,
                        'description': "123",
                        'roles': self.role,
                        'creator': self.TestUser,
                        'attack': 3,
                        'defense': 3,
                        'hp': 3,
                    },
                    files={
                        'image_url': file
                    }
                )
                self.assertTrue(form.is_valid())

    def test_form_valid_with_webp_image(self):
        file = SimpleUploadedFile('photo.webp', WEBP_HEADER, content_type='image/webp')

        with patch('cloudinary.uploader.upload_image', return_value='fake/photo'):
            with patch('cloudinary.forms.CloudinaryFileField.to_python', return_value='fake/photo'):
                form = CharacterForm(
                    data={
                        'name': 'Ivan',
                        'title': 'Ivanov',
                        'type': CharacterType.OTHER,
                        'description': "123",
                        'roles': self.role,
                        'creator': self.TestUser,
                        'attack': 3,
                        'defense': 3,
                        'hp': 3,
                    },
                    files={
                        'image_url': file
                    }
                )
                self.assertTrue(form.is_valid())

    def test_form_invalid_with_invalid_image_extension(self):
        file = SimpleUploadedFile('photo.gif', JPEG_HEADER, content_type='image/jpeg')

        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3,
        },
        files = {
            'image_url': file
        }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Only JPEG, PNG, and WebP images are allowed.', form.errors['image_url'])

    def test_form_invalid_with_fake_pdf_image_extension(self):
        file = SimpleUploadedFile('photo.pdf', FAKE_BYTES, content_type='image/jpeg')

        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3,
        },
        files = {
            'image_url': file
        }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Only JPEG, PNG, and WebP images are allowed.', form.errors['image_url'])

    def test_form_invalid_with_invalid_image_content_type(self):
        file = SimpleUploadedFile('photo.jpg', JPEG_HEADER, content_type='image/gif')

        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3,
        },
            files={
                'image_url': file
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Only JPEG, PNG, and WebP images are allowed.', form.errors['image_url'])

    def test_form_invalid_with_invalid_magic_bytes(self):
        file = SimpleUploadedFile('photo.jpg', FAKE_BYTES, content_type='image/jpeg')

        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3,
        },
            files={
                'image_url': file
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('File does not appear to be a valid image.', form.errors['image_url'])

    def test_form_invalid_with_invalid_fail_size(self):
        large_content = JPEG_HEADER + b'\x00' * (2 * 1024 * 1024)
        file = SimpleUploadedFile('photo.jpg', large_content, content_type='image/jpeg')

        form = CharacterForm(data={
            'name': 'Ivan',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3,
        },
            files={
                'image_url': file
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Image must not exceed 2MB.', form.errors['image_url'])

    def test_form_invalid_when_no_name(self):
        form = CharacterForm(data={
            'name': '',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Please enter the name of your character.",form.errors['name'])

    def test_form_invalid_when_title_and_name_are_same(self):
        form = CharacterForm(data={
            'name': 'Ivanov',
            'title': 'Ivanov',
            'type': CharacterType.OTHER,
            'description': "123",
            'roles': self.role,
            'creator': self.TestUser,
            'attack': 3,
            'defense': 3,
            'hp': 3
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Character name and title cannot be the same",form.errors['__all__'])