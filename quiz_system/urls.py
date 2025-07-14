from django.urls import path

from quiz_system import views

urlpatterns = [
    path('', views.QuizView.as_view(), name='start-quiz'),
    path('feedback/', views.FeedbackCreateView.as_view(), name='quiz-feedback')
]