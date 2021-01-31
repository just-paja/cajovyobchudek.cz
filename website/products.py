from django.urls import reverse


def get_tag_breadcrumbs(tags):
    return [
        {
            'label': tag.name,
            'url': reverse('website:catalog_tag', kwargs={'tag_id': tag.slug}),
        } for tag in tags
    ]


def get_main_ancestor(tag_ancestors):
    for ancestors in tag_ancestors:
        if ancestors[0].main_menu:
            return ancestors
    return tag_ancestors[0] or []


def get_product_breadcrumbs(tag_ancestors, product=None):
    ancestors = get_main_ancestor(tag_ancestors)
    breadcrumbs = get_tag_breadcrumbs(ancestors)
    if product:
        return breadcrumbs + [
            {
                'label': product.name,
                'url': reverse('website:product_detail', kwargs={'product_slug': product.slug}),
            }
        ]
    return breadcrumbs
