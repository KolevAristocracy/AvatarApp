from django.core.validators import MinLengthValidator
from django.db import models

from users.validators import LettersDigitsSpacesUnderscoreValidator


# Create your models here.

class User(models.Model):
    username = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(3),
            LettersDigitsSpacesUnderscoreValidator(),
        ]
    )
    password = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(8)],
        help_text="Password length requirements: 8 to 20 characters"
    )
    email = models.EmailField()
    age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

