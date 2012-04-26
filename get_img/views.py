from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response

from account.models import StoreImage

def get(request,name):
    Q = StoreImage.gql("WHERE name = :name", name=name)
    img = Q.get()
    if img:
        img=img.foto
    else:
        return HttpResponseNotFound()
    response = HttpResponse(img)
    response['Content-Type'] = 'image/png'
    return response
    

def _get_or_create_image(name):
    Q = StoreImage.gql("WHERE name = :name", name=name)
    img = Q.get()
    if img:
        return img
    else:
        return StoreImage(name=name)
    
