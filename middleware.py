from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def index(request):
    user_hash = request.session.get('my_au',None)
    user = user_hash
    return render_to_response('html/index.html',
                              {'user':user},
                              context_instance=RequestContext(request))
