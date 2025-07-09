from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from quiz_system.forms import QuizForm
from quiz_system.models import Question, Answer, UserAnswer


# Create your views here.

class QuizView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'quiz/quiz.html'
    login_url = reverse_lazy('login-user')

    def get_queryset(self):
        return Question.objects.prefetch_related('attribute').all()
    
    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_queryset()
        context['form'] = QuizForm(questions=questions)
        return context

    def post(self, request, *args, **kwargs):
        questions = self.get_queryset()
        form = QuizForm(request.POST, questions=questions)

        if form.is_valid():
            # Delete previous answers for current user
            UserAnswer.objects.filter(user=request.user).delete()

            scores = {
                'openness': 0,
                'conscientiousness': 0,
                'extraversion': 0,
                'agreeableness': 0,
                'neuroticism': 0,
            }

            user_answers_to_create = []

            for question in questions:
                answer = form.cleaned_data.get(f'question_{question.pk}')
                if answer:
                    user_answers_to_create.append(
                        UserAnswer(user=request.user, question=question, answer=answer)
                    )

                    # Adding scores data
                    attribute_name = question.attribute.name.lower()
                    if attribute_name in scores:
                        scores[attribute_name] += answer.score

            # Bulk create UserAnswer objects for better performance
            UserAnswer.objects.bulk_create(user_answers_to_create)

            # Update user's Profile with the scores
            profile = request.user.profile
            profile.openness = scores['openness']
            profile.conscientiousness = scores['conscientiousness']
            profile.extraversion = scores['extraversion']
            profile.agreeableness = scores['agreeableness']
            profile.neuroticism = scores['neuroticism']
            profile.save()

            return redirect(reverse_lazy('dashboard'))

        # if form is not valid return it again
        return render(request, self.template_name, {
            'questions': questions,
            'form': form,
        })


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
