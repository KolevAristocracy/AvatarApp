from django import forms

from quiz_system.models import Answer

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in self.questions:
            self.fields[f'question_{question.pk}'] = forms.ModelChoiceField(
                queryset=Answer.objects.all(), # 5 answers
                widget=forms.RadioSelect,
                label=question.text,
                empty_label=None,
                required=True,
            )

    def clean(self):
        cleaned_data = super().clean()
        for question in self.questions:
            field_name = f'question_{question.pk}'
            if field_name not in cleaned_data or not cleaned_data[field_name]: # checking if all questions are answered
                self.add_error(field_name, 'Please select an answer for the question.')

        return cleaned_data


