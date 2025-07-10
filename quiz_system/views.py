from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from quiz_system.forms import QuizForm
from quiz_system.models import Question, Answer, UserAnswer


# Create your views here.

class QuizView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'quiz/quiz_test.html'
    login_url = reverse_lazy('login-user')
    paginate_by = 4

    def get_queryset(self):
        return self.model.objects.prefetch_related('attribute').all().order_by('pk') # ordering them for better pagination

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)

        # ListView automatically provides the paginated questions in the page_obj
        questions_per_page = context['page_obj']
        context['form'] = QuizForm(questions=questions_per_page)
        return context

    def post(self, request, *args, **kwargs):
        # Get the paginator and the current page object
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Create a form instance with the submitted data and the questions for the current page
        form = QuizForm(request.POST, questions=page_obj)

        # Manually check if all questions are answered
        all_questions_answered = True
        for question in page_obj:
            field_name = f"question_{question.pk}"
            # If field for question on this page is missing from the POST data,
            # therefore the user did not answer it
            if not request.POST.get(field_name):
                all_questions_answered = False
                break # stop at the first missing answer

        if not all_questions_answered:
            messages.error(request, 'Please answer all questions before proceeding.')
            # Render the current page, passing the form back.
            # The form contains the user's submitted data
            return render(
                request,
                self.template_name,
                {
                    'form': form,
                    'page_obj': page_obj
                }
            )

        # If validation passes, saving the answers to the session
        quiz_answers = request.session.get('quiz_answers', {})

        for question in page_obj:
            field_name = f'question_{question.pk}'
            answer_id = request.POST.get(field_name)
            if answer_id:
                quiz_answers[str(question.pk)] = answer_id

        request.session['quiz_answers'] = quiz_answers

        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
            return redirect(f'{request.path}?page={next_page_number}')
        else:

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

            all_answers = request.session.get('quiz_answers', {})

            all_questions = Question.objects.in_bulk(list(all_answers.keys()))
            all_db_answers = Answer.objects.in_bulk(list(all_answers.values()))

            for question_pk, answer_pk in all_answers.items():
                question = all_questions.get(int(question_pk))
                answer = all_db_answers.get(int(answer_pk))
                if question and answer:
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

            del request.session['quiz_answers']

            return redirect(reverse_lazy('dashboard'))


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
