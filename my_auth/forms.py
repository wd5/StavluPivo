# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.api import mail

from django.conf import settings

from django import forms
from my_auth.models import User
from random import randint
import md5

class SignUp(forms.ModelForm):
    username = forms.CharField(max_length=30,required=True)
    #first_name = forms.CharField(max_length=30,required=False)
    #last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

    
    def clean_username(self):
        username = self.cleaned_data['username']
        cur = User.objects.filter(username=username)
        if cur:
            raise forms.ValidationError(_(u'Пользователь с таким именем уже существует!'))
        return self.cleaned_data['username']        
    
    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise forms.ValidationError(_('Passwords do not match.'))
        return self.cleaned_data['confirm_password']

    def save(self, *args, **kwargs):
        super(SignUp, self).save(*args, **kwargs)
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        password = self.cleaned_data['password']
        user.password = md5.md5(str(user.salt)+password).hexdigest()
        user.save()

        hash = md5.md5(user.username+user.email+user.password).hexdigest()
        url = 'http://%s/accounts/registration/%s/%s/'%(settings.MAIN_HOST,user.id,hash)
        #print url
        mail.send_mail(sender=settings.EMAIL_NOTIFICATION,
                       to=user.email,
                       subject="Подтверджение регистрации.",
                       body="Для подтверждения регистрации перейдите по указанной ссылке:\n"+url)

        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        if not self.cleaned_data.has_key('username'):
            raise
        username = self.cleaned_data['username']
        cur = User.objects.filter(username=username)
        if not cur:
            raise forms.ValidationError(_(u'Пользователя с таким именем не существует!'))
        return self.cleaned_data['username']        

    def clean_password(self):
        #username = self.clean_username()
        #if not username:
        #    raise
        if not self.cleaned_data.has_key('username'):
            return None
        username = self.cleaned_data['username']
        cur = User.objects.filter(username=username)
        password = self.cleaned_data['password']
        user=cur[0]
        if user.password != md5.md5(str(user.salt)+password).hexdigest():
            raise forms.ValidationError(_(u'Не верный пароль!'))
        return self.cleaned_data['password']        

