from django.urls import path
from quiz_system.views import start_quiz

urlpatterns = [
    path('quiz/', start_quiz, name='start-quiz'),
]