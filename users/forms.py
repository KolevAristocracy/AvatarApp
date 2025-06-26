from django import forms

from users.models import User


class UserBaseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }



class UserRegisterForm(UserBaseForm):
    ...


class UserLoginForm(UserBaseForm):
    class Meta(UserBaseForm.Meta):
        exclude = ['age', 'email']


class EditUserForm(UserBaseForm):
    ...

