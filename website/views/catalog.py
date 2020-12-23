from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render

from ..mapping import catalog_mapping


@require_http_methods(['GET'])
def home(req):
    return render(req, 'catalog.html')


@require_http_methods(['GET'])
def category(req, category_id):
    item = catalog_mapping[category_id]
    try:
        if item:
            return render(req, 'catalog/%s' % item['template'])
    except TemplateDoesNotExist:
        raise Http404
    raise Http404
