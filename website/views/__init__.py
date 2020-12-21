from django.views.decorators.http import require_http_methods
from django.shortcuts import render


@require_http_methods(['GET'])
def home(req):
    return render(req, 'home.html')


@require_http_methods(['GET'])
def contact(req):
    return render(req, 'contact.html')
