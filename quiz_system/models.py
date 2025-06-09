from django.contrib.auth.models import User
from django.db import models

from attributes.models import Attribute

# Create your models here.

class Question(models.Model):
    text = models.TextField()
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    score = models.PositiveIntegerField()
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} (+{self.score} {self.attribute})"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)