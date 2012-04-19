# -*- coding: utf-8 -*-
 
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson

#from django.contrib.auth.decorators import login_required
from my_auth.decorators import login_required

from account.models import WallTask
from my_auth.models import User
import base64

from my_auth.forms import SignUp

@login_required
def main_page(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    context={'user':u}
    return render_to_response('html/accounts.html',
                              context,
                              context_instance=RequestContext(request))

@login_required
def wall_page(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    context={'user':u}
    context['tasks'] = WallTask.objects.filter(owner=u)
    return render_to_response('html/wall.html',
                              context,
                              context_instance=RequestContext(request))

@login_required
def add_wall_task(request):
    errors = []
    d = {}
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = User.objects.filter(id=int(s))
    if not u:
        errors.append('Вы должны авторизоваться')
    else:
        u=u[0]
    try:
        d['title'] = request.GET['title']
        d['text'] = request.GET['text']
        d['x'] = request.GET['x']
        d['y'] = request.GET['y']
    except:
        errors.append('Указаны не все параметры!')
    if not errors:
        wt=WallTask(title=d['title'],text_task=d['text'],position_x=d['x'],position_y=d['y'], owner=u)
        d['user'] = u.username
        wt.save()
        d['id'] = wt.id
    return HttpResponse(simplejson.dumps({'errors':errors,'data':d}),
                        mimetype='text/json')

def del_wall_task(request,task_id):
    t = WallTask.objects.get(id=task_id)
    if t:
        t.delete();
    return HttpResponse('Ok',mimetype='text/plain')


def signup(request):
    if request.method=='POST':
        form = SignUp(request.POST)
        er = form.to_model()
        if er:
            for key in er:
                form.errors[key] = er[key]
            context = {'form' : form}
        else:
            return HttpResponseRedirect('/')
    if request.method=='GET':
        context = {'form' : SignUp()}
    return render_to_response('html/signup.html',
                              context,
                              context_instance=RequestContext(request))
