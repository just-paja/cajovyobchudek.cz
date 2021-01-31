from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from cajovyobchudek.models import Product, Tag


@require_http_methods(['GET'])
def home(req):
    return render(req, 'catalog/index.html')


def get_breadcrumbs(tags):
    return [
        {
            'label': tag.name,
            'url': reverse('website:catalog_tag', kwargs={'tag_id': tag.slug}),
        } for tag in tags
    ]


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
        'tag': tag_item,
        'products': products,
        'breadcrumbs': get_breadcrumbs(ancestors),
        'subordinates': subordinates,
    })


def get_main_ancestor(tag_ancestors):
    for ancestors in tag_ancestors:
        if ancestors[0].main_menu:
            return ancestors
    return tag_ancestors[0]


def get_product_breadcrumbs(product, tag_ancestors):
    ancestors = get_main_ancestor(tag_ancestors)
    if not ancestors:
        return []
    return get_breadcrumbs(ancestors) + [
        {
            'label': product.name,
            'url': reverse('website:product_detail', kwargs={'product_slug': product.slug}),
        }
    ]


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
    return render(req, 'catalog/product.html', {
        'breadcrumbs': get_product_breadcrumbs(product, tag_ancestors),
        'product': product,
        'description': product.description,
        'usage': product.usage,
    })
