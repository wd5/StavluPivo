import urllib

from django.http import HttpResponseRedirect

#def test_login(view_func):
def login_required(view_func):
    def new(request, *args, **kwargs):
        u = request.session.get('my_au',None)
        if u:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/accounts/login/?'+ urllib.urlencode({'redirect_to':request.path}))
    return new

#def login_required(function=None):
#    actual_decorator
