# -*- coding: utf-8 -*-
 
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse

#from django.contrib.auth.decorators import login_required
from my_auth.decorators import login_required

from my_auth.models import User
from my_auth.forms import SignUp, LoginForm

from account.models import StoreImage
from account.forms import ContactForm, HelpForm, HelpMeForm, FullProfile

from google.appengine.ext import db

from get_img.views import _get_or_create_image

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
    ## Функционал приостановлен
    return render_to_response('html/fun-inactive.html',
                                  {},
                                  context_instance=RequestContext(request))
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

@login_required
def set_contact(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    if u.contact:
        return HttpResponseRedirect(reverse(main_page))
    if request.method=='POST':
        form = ContactForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(u)
            _save_avatar(request,u)
            #if request.FILES.has_key('foto'):
            #    foto = request.FILES['foto']
            #    name = '%s-avatar.%s'%(u.id,foto.name.split('.')[-1])
            #    storeimage = _get_or_create_image(name) #StoreImage()
            #    storeimage.foto = db.Blob(foto.read())
            #    #storeimage.name = name
            #    storeimage.put()
            #    u.contact.foto=storeimage.name
            #    u.contact.save()
            return HttpResponseRedirect(reverse('set_help'))
    else:
        if u.contact:
            form = ContactForm(instance=u.contact)
        else:
            form = ContactForm()
    context={'user': u,
             'form' : form}
    return render_to_response('html/account-wizard/contact.html',
                              context,
                              context_instance=RequestContext(request))

@login_required
def set_help(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    if not u.contact:
        return HttpResponseRedirect(reverse('set_contact'))
    else:
        if u.contact.help_types:
            return HttpResponseRedirect(reverse(main_page))
    if request.method=='POST':
        form = HelpForm(request.POST,instance=u.contact)
        if form.is_valid():
            form.save()
            request.session['helpme']=True
            return HttpResponseRedirect(reverse(set_help_me))
    else:
        form = HelpForm(instance=u.contact)
    return render_to_response('html/account-wizard/help.html',
                                      {'user': u,
                                       'form':form},
                                      context_instance=RequestContext(request))     

@login_required
def set_help_me(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    if not request.session.get('helpme',False):
        return HttpResponseRedirect(reverse(set_contact))        
    if not u.contact:
        return HttpResponseRedirect(reverse('set_contact'))
    if request.method=='POST':
        form = HelpMeForm(request.POST,instance=u.contact)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(main_page))
        
    else:
        form = HelpMeForm(instance=u.contact)
    return render_to_response('html/account-wizard/help_me.html',
                                      {'user': u,
                                       'form':form},
                                      context_instance=RequestContext(request))     

@login_required
def edit_contact(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
    if not u.contact:
        return HttpResponseRedirect(reverse(set_contact))
    if request.method=='POST':
        form = FullProfile(request.POST,instance=u.contact)
        if form.is_valid():
            form.save()
            _save_avatar(request,u)
            return HttpResponseRedirect(reverse(main_page))
    else:
        form = FullProfile(instance = u.contact)
    return render_to_response('html/account-wizard/full-edit.html',
                                      {'user': u,
                                       'form':form
                                       },
                                      context_instance=RequestContext(request))     
    
def _save_avatar(request,user,file_name='foto'):
    if request.FILES.has_key(file_name):
        foto = request.FILES[file_name]
        name = '%s-avatar.%s'%(user.id,foto.name.split('.')[-1])
        storeimage = _get_or_create_image(name) #StoreImage()
        storeimage.foto = db.Blob(foto.read())
        #storeimage.name = name
        storeimage.put()
        user.contact.foto=storeimage.name
        user.contact.save()
