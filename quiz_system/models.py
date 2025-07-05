from django.db import models

from accounts.models import CustomUser
from attributes.models import Attribute

# Create your models here.

class Question(models.Model):
    text = models.TextField()
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200)
    score = models.PositiveIntegerField()
    # Using signal to create default answers and score for each question

    def __str__(self):
        return f"{self.text} ({self.score})"


class UserAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)