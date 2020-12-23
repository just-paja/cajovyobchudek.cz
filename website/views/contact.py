from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from cajovyobchudek.models import BusinessHours


@require_http_methods(['GET'])
def home(req):
    business_days = BusinessHours.get_weekdays()
    return render(req, 'contact.html', {
        'business_days': business_days.items()
    })
