from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render

from cajovyobchudek.models import Tag


@require_http_methods(['GET'])
def home(req):
    return render(req, 'catalog/index.html')


@require_http_methods(['GET'])
def tag(req, tag_id):
    try:
        tag_item = Tag.objects.get(slug=tag_id, public=True)
    except Tag.DoesNotExist:
        raise Http404
    return render(req, 'catalog/tag.html', {
        'tag': tag_item,
        'subordinates': tag_item.subordinate_tags
    })
