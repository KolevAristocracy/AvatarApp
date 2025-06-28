from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=0)
