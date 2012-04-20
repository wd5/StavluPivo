# -*- coding: utf-8 -*-
 
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson

#from django.contrib.auth.decorators import login_required
from my_auth.decorators import login_required

from account.models import WallTask
from my_auth.models import User

from my_auth.forms import SignUp, LoginForm

import md5
import base64

@login_required
def main_page(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    context={'user':u}
    return render_to_response('html/accounts.html',
                              context,
                              context_instance=RequestContext(request))


def signup(request):
    form = SignUp()
    form_login = LoginForm()
    
    if request.method=='POST':
        if request.POST['flag']=='r':
            form = SignUp(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                user = User.objects.get(username=form_login.cleaned_data['username'])
                request.session['my_au'] = base64.encodestring('user_id=%s;activ=%s;su=%s'%(user.id,user.is_active,user.is_superuser))
                return HttpResponseRedirect('/accounts/')
            
    #if request.method=='GET':
    context = {'form' : form,
               'form_login' : form_login
               }
    return render_to_response('html/signup.html',
                              context,
                              context_instance=RequestContext(request))

def registration(request,id,hash):
    user = get_object_or_404(User,id=id)
    if hash == md5.md5(user.username+user.email+user.password).hexdigest():
        user.is_active = True
        user.save()
        request.session['my_au'] = base64.encodestring('user_id=%s;activ=%s;su=%s'%(user.id,user.is_active,user.is_superuser))
        return render_to_response('html/thanks-registration.html',
                                  {'user':user},
                                  context_instance=RequestContext(request))
    return HttpResponseNotFound()
