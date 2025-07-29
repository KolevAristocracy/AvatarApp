from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.validators import LettersDigitsSpacesUnderscoreValidator

UserModel = get_user_model()


class TestUsernameIsValid(TestCase):
    def setUp(self):
        self.validator = LettersDigitsSpacesUnderscoreValidator()
        self.message = '*Allowed names contain letters, digits, spaces, and underscores.'
        self.invalid_username = "Inv@a!id U$ername"
        self.valid_username = "TestUser1"


    def test__username_is_valid(self):
        # not need to writing anything more because the validator will raise
        # error if invalid
        self.validator(self.valid_username)

    def test__username_is_invalid__raise_ValidationError(self):
        with self.assertRaises(ValidationError) as ve:
            self.validator(self.invalid_username)

        self.assertEqual(str(ve.exception), f"{[self.message]}")