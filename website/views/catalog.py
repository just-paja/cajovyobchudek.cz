from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render

from cajovyobchudek.models import Product, Tag


@require_http_methods(['GET'])
def home(req):
    return render(req, 'catalog/index.html')


@require_http_methods(['GET'])
def tag(req, tag_id):
    try:
        tag_item = Tag.objects.get(slug=tag_id, public=True)
    except Tag.DoesNotExist:
        raise Http404

    subordinates = tag_item.get_children().filter(public=True).all()
    ancestors = tag_item.get_ancestors(include_self=True).filter(public=True).all()
    products = Product.objects.filter(
        public=True,
        product_tags__tag__public=True,
        product_tags__tag__lft__gte=tag_item.lft,
        product_tags__tag__rght__lte=tag_item.rght,
    ).distinct()
    if len(ancestors) == 1:
        ancestors = []
    return render(req, 'catalog/tag.html', {
        'tag': tag_item,
        'products': products,
        'ancestors': ancestors,
        'subordinates': subordinates,
    })
