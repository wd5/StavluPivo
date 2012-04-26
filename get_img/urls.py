from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('get_img.views',
                       url(r'(?P<name>[\w\d\.-]+)$','get', name='get'),
                       )
