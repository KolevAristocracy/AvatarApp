from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from quiz_system.models import Question


# Create your views here.

class QuizView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'quiz/quiz.html'
    login_url = reverse_lazy('login-user')


    def post(self, request, *args, **kwargs):
        request.session['answers'] = request.POST.dict()
        return redirect(reverse_lazy('dashboard:results'))


# def start_quiz(request):
#     questions = Question.objects.prefetch_related('answer_set').all()
#
#     context = {
#         'questions': questions,
#     }
#
#     if request.method == "POST":
#         request.session['answers'] = request.POST
#         return redirect('dashboard/result.html')
#
#     return render(request, 'quiz/quiz.html', context)
