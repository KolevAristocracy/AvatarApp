from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()

class TestUserModel(TestCase):

    def test__valid_str_method__returns_email(self):
        # Arrange
        email = 'test12@test.com'
        user = UserModel.objects.create_user( # create_user() to hash the password
            username='TestUsername',
            email=email,
            password='12test34',
        )


        # Act & Assert
        self.assertEqual(email, str(user))
