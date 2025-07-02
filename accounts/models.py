from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import OneToOneField

from accounts.managers import CustomUserManager
from accounts.validators import LettersDigitsSpacesUnderscoreValidator


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    username = models.CharField(
        max_length=20,
        validators=[LettersDigitsSpacesUnderscoreValidator()],
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        null=True,
        blank=True,
    )

    openness = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    conscientiousness = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    extraversion = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    agreeableness = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    
    neuroticism = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )