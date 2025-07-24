from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile, CustomUser

UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'Username or Email'


class EditUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', ]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="New password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New password"
    )

    def __init__(self, user: CustomUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The new passwords do not match.")
            password_validation.validate_password(new_password1, self.user)
        return cleaned_data


class ContactForm(forms.Form):
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email",
            }
        ),
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter your message here...",
                'rows': 6,
            }
        ),
    )
