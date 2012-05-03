# -*- coding:utf-8 -*-

from django.db import models
#from my_auth.models import User
from django.utils.translation import ugettext as _

from google.appengine.ext import db


class StoreImage(db.Model):
    foto = db.BlobProperty()
    name = db.StringProperty()

#storeimage.foto = db.Blob(avatar)
#storeimage.put()

class Contact(models.Model):
    #foto = models.ImageField(upload_to='files/upload',blank=True)
    foto = models.CharField(_(u'Файл'),max_length=128, blank=True)
    first_name = models.CharField(_(u'Имя'), max_length=30, blank=False)
    phone = models.CharField(_(u'Телефон'),max_length=20, blank=True)
    land = models.CharField(_(u'Страна'),max_length=20, blank=True)
    city = models.CharField(_(u'Город'),max_length=20, blank=True)

    help_types = models.CharField(_(u'Типы помощи'),max_length=64, blank=False)
    help_description = models.TextField(_(u'Описание'), blank=True)

    help_me_flag = models.BooleanField(_(u'Я не нуждаюсь в помощи'),blank=False)
    help_me_description = models.TextField(_(u'Описание'), blank=True)
    help_me_types = models.CharField(_(u'Типы помощи'),max_length=64, blank=True)
    
    def __unicode__(self):
        return self.first_name

