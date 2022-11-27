from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CreateUser(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    name = forms.CharField(label='Имя', widget=forms.TextInput(), required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())
    agree_statement = forms.BooleanField(label='', help_text='Some text you need to agree with', widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'name',  'password1', 'password2', 'agree_statement')

class LoginUser(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        #widgets = {
        #    'comment_content': forms.Textarea(),
        #}



