from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('account.views',
                       url(r'^$','main_page', name='account_main_page'),
                       url(r'^signup/$', 'signup', name='add_user'),
                       url(r'^registration/(?P<id>\d+)/(?P<hash>[\w\d]+)/$','registration', name='registration'),
                       url(r'^wizard/contact-info/','set_contact',name='set_contact'),
                       url(r'^wizard/help/','set_help',name='set_help'),
                       url(r'^wizard/help-me/','set_help_me',name='set_help_me'),
                       url(r'^edit/','edit_contact',name='edit_contact'),

#                       url(r'wall/$','wall_page', name='account_wall_page'),
#                       url(r'wall/add-task','add_wall_task', name='add_wall_task'),
#                       url(r'wall/(?P<task_id>\d+)/del-task/','del_wall_task', name='del_wall_task'),
                       )
