# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from account.models import Contact

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=256)

class ContactForm(forms.ModelForm):
    foto = forms.ImageField(required=False)
    first_name = forms.CharField(label=u'Имя *', max_length=30, required=True)
    phone = forms.CharField(label=u'Телефон',max_length=20, required=False)
    land = forms.CharField(label=u'Страна',max_length=20, required=False)
    city = forms.CharField(label=u'Город',max_length=20, required=False)

    class Meta():
        model = Contact
        fields = ('foto','first_name','phone', 'land', 'city')

    def save(self, user, *args, **kwargs):
        super(ContactForm, self).save(*args, **kwargs)
        user.contact = self.instance
        user.save()


class HelpForm(forms.ModelForm):
    help_types = forms.MultipleChoiceField(
        choices=(('consultation',u'Консультация'),
                 ('home',u'Бытовая помощь'),
                 ('transport',u'Транспортные услуги'),
                 ('other',u'Другое')
                 ), 
        label="Я могу помочь: ",
        widget=forms.CheckboxSelectMultiple,
        required=True) 

    class Meta():
        model = Contact
        fields = ('help_description',)

    def save(self, *args, **kwargs):
        super(HelpForm, self).save(*args, **kwargs)
        self.instance.help_types = str(self.cleaned_data['help_types'])
        self.instance.save()
    
    
