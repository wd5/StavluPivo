from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

import md5
from my_auth.models import User

import base64

def login(request):
    if request.method == 'POST':
        try:
            redirect_to = request.POST['redirect_to']
        except:
            redirect_to = '/accounts/'
        err={}
        username = request.POST['username']
        if not username:
            err['username'] = ['Field "username" is requered!']
        password = request.POST['password']
        if not password:
            err['password'] = ['Field "password" is requered!']
        if err:
            return render_to_response(
                'html/login.html',
                {'errors' : err, 'redirect_to' : redirect_to},
                context_instance=RequestContext(request)
                )
        user=User.objects.filter(username=username)
        if not user:
            err['username'] = ['User "%s" not find!'%(username,)]
        else:
            user=user[0]
            if user.password != md5.md5(str(user.salt)+password).hexdigest():
                err['password'] = ['Password is failed!']
        if err:
            return render_to_response(
                'html/login.html',
                {'errors' : err, 'redirect_to' : redirect_to},
                context_instance=RequestContext(request)
                )
        request.session['my_au'] = base64.encodestring('user_id=%s;activ=%s;su=%s'%(user.id,user.is_active,user.is_superuser))
        return HttpResponseRedirect(redirect_to)
    try:
        redirect_to = request.GET['redirect_to']
    except:
        redirect_to = '/accounts/'
    return render_to_response(
        'html/login.html',
        {'redirect_to' : redirect_to},
        context_instance=RequestContext(request)
        )

def logout(request):
    request.session['my_au'] = None
    return HttpResponseRedirect('/')

        
        

