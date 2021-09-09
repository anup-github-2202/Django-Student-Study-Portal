from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search  ")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]

    ############---------------------------- UserCreationForm----------------------------#####################
    # <QueryDict: {'csrfmiddlewaretoken': ['Hob7M2CMXo7PzHHQtumgivWKcpUbMbqHIH2O2B0G3dCkl7zunfDJ4oJf4YgZr88J'],
    # 'password': ['anup2345'], 'last_login': ['today'], 'is_superuser': ['on'], 'user_permissions': ['22'],
    # 'username': ['anup2345'], 'first_name': ['anup'], 'last_name': ['burnwal'], 'email': ['anup2345@gmail'],
    # 'is_staff': ['on'], 'is_active': ['on'], 'date_joined': ['2021-09-07 11:13:30'], 'initial-date_joined': [
    # '2021-09-07 11:13:30'], 'password1': ['anup2345'], #	'password2': ['anup2345']}>
