from django.db import models
from django.template.defaultfilters import truncatewords


# Create your models here.

class Attribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # @property
    # def short_description(self):
    #     return truncatewords(self.description, 15)

    def __str__(self):
        return self.name