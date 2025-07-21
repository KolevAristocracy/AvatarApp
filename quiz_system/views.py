from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from attributes.models import Attribute
from quiz_system.forms import QuizForm, FeedbackForm
from quiz_system.models import Question, Answer, UserAnswer, Feedback


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
        page_obj = context['page_obj']
        current_page = page_obj.number

        # Preventing user to skip to the last page of quiz without answer all questions
        last_allowed_page = self.request.session.get('quiz_last_page', 1)

        if current_page > last_allowed_page:
            messages.warning(self.request, "Please complete the quiz in order.")
            paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
            page_obj = paginator.get_page(last_allowed_page)
            context['page_obj'] = page_obj
            current_page = last_allowed_page

        context['form'] = self.get_form(page_obj)
        return context

    def get_form(self, page_obj, data=None):
        return QuizForm(data, questions=page_obj)

    def post(self, request: HttpRequest, *args, **kwargs):
        page_obj = self._get_page_obj(request)
        form = self.get_form(page_obj, request.POST)

        if not form.is_valid():
            messages.error(request, 'Please answer all questions before proceeding.')
            return render(request, self.template_name, {'form': form, 'page_obj': page_obj})

        # If validation passes, saving the answers to the session
        self._save_answers_to_session(request, form.cleaned_data)

        if page_obj.has_next():
            request.session['quiz_last_page'] = page_obj.next_page_number()
            return redirect(f'{request.path}?page={page_obj.next_page_number()}')
        else:
            request.session.pop('quiz_last_page', None)
            self._finalize_quiz(request)
            return redirect('dashboard')


    def _get_page_obj(self, request: HttpRequest):
        paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
        page_number = request.GET.get('page', 1)
        return paginator.get_page(page_number)

    def _save_answers_to_session(self, request: HttpRequest, cleaned_data):
        quiz_answers = request.session.get('quiz_answers', {})

        for field_name ,answer in cleaned_data.items():
            question_pk = field_name.replace('question_', '')
            quiz_answers[question_pk] = str(answer.pk)

        request.session['quiz_answers'] = quiz_answers

    def _finalize_quiz(self, request):
        # Deleting old test score
        UserAnswer.objects.filter(user=request.user).delete()

        scores = {attr.name.lower(): 0 for attr in  Attribute.objects.all()}
        answer_data = request.session.get('quiz_answers', {})

        question_ids = list(map(int, answer_data.keys()))
        answer_ids = list(map(int, answer_data.values()))

        questions = Question.objects.in_bulk(question_ids)
        answers = Answer.objects.in_bulk(answer_ids)

        user_answers = []

        for q_id, a_id in answer_data.items():
            question = questions.get(int(q_id))
            answer = answers.get(int(a_id))
            if question and answer:
                user_answers.append(UserAnswer(user=request.user, question=question, answer=answer))
                attr_name = question.attribute.name.lower()
                if attr_name in scores:
                    scores[attr_name] += answer.score

        UserAnswer.objects.bulk_create(user_answers)

        # Save scores to user profile

        profile = request.user.profile
        profile.openness = scores['openness']
        profile.conscientiousness = scores['conscientiousness']
        profile.extraversion = scores['extraversion']
        profile.agreeableness = scores['agreeableness']
        profile.neuroticism = scores['neuroticism']
        profile.save()

        # Clear session
        del request.session['quiz_answers']


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'quiz/feedback.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)