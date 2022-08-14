from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.db import transaction
from .models import Book, User


class Bookform(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        exclude = ('user',)


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        ]
        field_classes = {"username": UsernameField}

    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user
