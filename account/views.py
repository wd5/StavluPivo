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

from account.forms import ContactForm, HelpForm

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

@login_required
def set_contact(request):
    s = base64.decodestring(request.session['my_au']).split(';')[0].split('=')[1]
    u = get_object_or_404(User,id=s)
#    if u.contact:
#        return HttpResponseRedirect(reverse(main_page))
    if request.method=='POST':
        form = ContactForm(request.POST)
        #file_var=request.FILES[file_name]
        #path = settings.SECURITY_MEDIA_ROOT+'/vars/'+str(campaign.id)+'.xls'
        #tmp_f = open(path,'wb')
        #tmp_f.write(file_var.read())
        #tmp_f.close()
        if form.is_valid():
            form.save(u)
            #if request.FILES.has_key('foto'):
            #    foto = request.FILES['foto']
            #    path = settings.MEDIA_ROOT+'/load-files/avatar-'+str(u.id)+foto.name
            #    tmp_f = open(path,'wb')
            #    tmp_f.write(foto.read())
            #    tmp_f.close()
            #    u.contact.foto=settings.MEDIA_URL+'load-files/avatar-'+str(u.id)+foto.name
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
    if request.method=='POST':
        form = HelpForm(request.POST,instance=u.contact)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(main_page))
    else:
        form = HelpForm(instance=u.contact)
    return render_to_response('html/account-wizard/help.html',
                                      {'user': u,
                                       'form':form},
                                      context_instance=RequestContext(request))     

