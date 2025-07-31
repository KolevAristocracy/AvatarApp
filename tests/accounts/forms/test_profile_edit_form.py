from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import EditUserForm

UserModel = get_user_model()


class TestUserProfileEdit(TestCase):
    def setUp(self):
        # signal creates profile after user is registered
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='12test34',
        )
        self.profile = self.user.profile


    def test_initial_data_is_none(self):
        self.assertIsNone(self.profile.first_name)
        self.assertIsNone(self.profile.last_name)
        self.assertIsNone(self.profile.age)

    def test_negative_age_not_valid(self):
        form = EditUserForm(data={
            'age': -1,
        }, instance=self.profile)

        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
        self.assertIsNone(self.profile.age)

    def test_valid_age_changes_successfully(self):
        form = EditUserForm(data={
            'age': 25,
        }, instance=self.profile)

        self.assertTrue(form.is_valid())
        form.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.age, 25)
