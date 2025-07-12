from django import forms

from quiz_system.models import Answer

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        # relevant_answer_ids = Answer.objects.filter(question__in=self.questions).values_list('pk', flat=True)

        for question in self.questions:
            self.fields[f'question_{question.pk}'] = forms.ModelChoiceField(
                queryset=Answer.objects.all(), # 5 answers
                widget=forms.RadioSelect,
                label=question.text,
                empty_label=None,
                required=True,
            )
