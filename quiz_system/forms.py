from django import forms

from quiz_system.models import Answer, Feedback


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


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'message': 'Your Feedback',
        }