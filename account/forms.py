# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from account.models import Contact

TYPE_CHOICES =(('consultation',u'Консультация'),
                 ('home',u'Бытовая помощь'),
                 ('transport',u'Транспортные услуги'),
                 ('other',u'Другое')
                 )

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=256)

class ContactForm(forms.ModelForm):
    foto = forms.ImageField(required=False)
#    first_name = forms.CharField(label=u'Имя *', max_length=30, required=True)
#    phone = forms.CharField(label=u'Телефон',max_length=20, required=False)
#    land = forms.CharField(label=u'Страна',max_length=20, required=False)
#    city = forms.CharField(label=u'Город',max_length=20, required=False)

    class Meta():
        model = Contact
        fields = ('first_name','phone', 'land', 'city')

    def save(self, user, *args, **kwargs):
        super(ContactForm, self).save(*args, **kwargs)
        user.contact = self.instance
        user.save()


class HelpForm(forms.ModelForm):
    help_types = forms.MultipleChoiceField(
        choices=TYPE_CHOICES,
        label="Я могу помочь: ",
        widget=forms.CheckboxSelectMultiple,
        required=True) 

    class Meta():
        model = Contact
        fields = ('help_description',)

    def save(self, *args, **kwargs):
        super(HelpForm, self).save(*args, **kwargs)
        data = reduce(lambda x,y:x+' '+y,self.cleaned_data['help_types'])
        self.instance.help_types = data
        self.instance.save()


class HelpMeForm(forms.ModelForm):
    help_me_types = forms.MultipleChoiceField(
        choices=TYPE_CHOICES,
        label="Я могу помочь: ",
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta():
        model = Contact
        fields = ('help_me_description','help_me_flag')

    def save(self, *args, **kwargs):
        super(HelpMeForm, self).save(*args, **kwargs)
        data_me = self.cleaned_data['help_me_types']
        if data_me:
            data_me = reduce(lambda x,y:x+' '+y,data_me)
        else:
            data_me = ''
        self.instance.help_me_types = data_me
        self.instance.save()

    
class FullProfile(forms.ModelForm):
    foto = forms.ImageField(required=False)
    help_types = forms.MultipleChoiceField(
        choices=TYPE_CHOICES,
        label="Я могу помочь: ",
        widget=forms.CheckboxSelectMultiple,
        required=True) 
    help_me_types = forms.MultipleChoiceField(
        choices=TYPE_CHOICES,
        label="Я могу помочь: ",
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta():
        model = Contact
        fields = ('first_name','phone', 'land', 'city', 'help_description','help_me_description','help_me_flag')
    
    def save(self, *args, **kwargs):
        super(FullProfile, self).save(*args, **kwargs)
        data = reduce(lambda x,y:x+' '+y,self.cleaned_data['help_types'])
        data_me = self.cleaned_data['help_me_types']
        if data_me:
            data_me = reduce(lambda x,y:x+' '+y,data_me)
        else:
            data_me = ''
        self.instance.help_types = data
        self.instance.help_me_types = data_me
        self.instance.save()
