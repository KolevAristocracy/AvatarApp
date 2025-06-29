from django.urls import path

from quiz_system.views import QuizView

urlpatterns = [
    path('', QuizView.as_view(), name='start-quiz'),
]