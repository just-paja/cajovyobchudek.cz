from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render

from cajovyobchudek.models import Product, Tag

from ..products import get_product_breadcrumbs, get_tag_breadcrumbs
from ..title import get_page_title


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
    return render(req, 'catalog/tag.html', {
        'breadcrumbs': get_tag_breadcrumbs(ancestors),
        'products': products,
        'subordinates': subordinates,
        'page_title': get_page_title(tag_item.name),
        'tag': tag_item,
    })


@require_http_methods(['GET'])
def product_detail(req, product_slug):
    try:
        product = Product.objects.prefetch_related('product_tags__tag').get(
            slug=product_slug,
            public=True
        )
    except Product.DoesNotExist:
        raise Http404

    product_tags = product.product_tags.order_by('tag__lft').all()
    tag_ancestors = [
        tag_item.tag.get_ancestors(
            include_self=True
        ).filter(public=True).all() for tag_item in product_tags
    ]
    variants = product.variants.filter(public=True).all()
    return render(req, 'catalog/product.html', {
        'breadcrumbs': get_product_breadcrumbs(tag_ancestors, product),
        'description': product.description,
        'page_title': get_page_title(product.name),
        'product': product,
        'usage': product.usage,
        'variants': variants,
    })
