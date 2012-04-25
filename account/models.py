# -*- coding:utf-8 -*-

from django.db import models
#from my_auth.models import User
from django.utils.translation import ugettext as _

from google.appengine.ext import db

class Contact(models.Model):
    foto = models.ImageField(upload_to='files/upload')
    #foto = db.BlobProperty(required=False)
    first_name = models.CharField(_(u'Имя'), max_length=30, blank=True)
    phone = models.CharField(_(u'Телефон'),max_length=20, blank=False)
    land = models.CharField(_(u'Страна'),max_length=20, blank=False)
    city = models.CharField(_(u'Город'),max_length=20, blank=False)

    help_types = models.CharField(_(u'Типы помощи'),max_length=64, blank=False)
    help_description = models.TextField(_(u'Описание'), blank=True)

    def __unicode__(self):
        return self.first_name

