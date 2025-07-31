from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import ChangePasswordForm

UserModel = get_user_model()


class TestChangePasswordForm(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12test34'
        )

    def test_valid_password_change(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                'old_password': '12test34',
                'new_password1': '12newpass34',
                'new_password2': '12newpass34',
            }
        )
        self.assertTrue(form.is_valid())


    def test_invalid_old_password(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                'old_password': 'WrongPassword12',
                'new_password1': '12newpass34',
                'new_password2': '12newpass34',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
        self.assertIn('Old password is incorrect.', form.errors['old_password'])


    def test_new_passwords_do_not_match(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                'old_password': '12test34',
                'new_password1': '12newpass34',
                'new_password2': '12wrongpass34',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("The new passwords do not match.", form.errors['__all__'])


    def test_new_password_fails_validation__its_to_simple(self):
        error_msgs = [
            'This password is too short. It must contain at least 8 characters.',
            'This password is too common.',
            'This password is entirely numeric.'
        ]
        form = ChangePasswordForm(
            user=self.user,
            data={
                'old_password': '12test34',
                'new_password1': '1234',
                'new_password2': '1234',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn(error_msgs[0], form.errors['__all__'])
        self.assertIn(error_msgs[1], form.errors['__all__'])
        self.assertIn(error_msgs[2], form.errors['__all__'])