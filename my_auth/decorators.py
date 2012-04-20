import urllib

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from my_auth.models import User
import base64

#def test_login(view_func):
def login_required(view_func):
    def new(request, *args, **kwargs):
        u = request.session.get('my_au',None)
        if u:
            s = base64.decodestring(u).split(';')[0].split('=')[1]
            u = get_object_or_404(User,id=s)
            if u.is_active:
                return view_func(request, *args, **kwargs)
            else:
                return render_to_response('html/error-registration.html',
                                          {'user':u},
                                          context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/accounts/login/?'+ urllib.urlencode({'redirect_to':request.path}))
    return new

#def login_required(function=None):
#    actual_decorator
