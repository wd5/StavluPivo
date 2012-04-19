# -*- coding: utf-8 -*-

from django import forms
from my_auth.models import User
from random import randint
import md5

class SignUp(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    email = forms.CharField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def to_model(self):
        if not self.is_valid():
            return dict(self.errors)
        username = self.cleaned_data['username']
        cur = User.objects.filter(username=username)
        if cur:
            return {'username':['Пользователь с таким именем уже существует!']}
        n = randint(0,1000000)
        password = md5.md5(str(n) + self.cleaned_data['password']).hexdigest()
        u = User(username=username,
                 first_name=self.cleaned_data['first_name'],
                 last_name=self.cleaned_data['last_name'],
                 email=self.cleaned_data['email'],
                 salt=n,
                 password=password,
                 )
        u.save()
        return None
    
