from cajovyobchudek.models import BusinessHours, SiteAlert, Tag

from .title import SITE_NAME


def exclude_admin(func):
    def inner(request):
        if '/admin' not in request.META.get('PATH_INFO', ''):
            return func(request)
        return {}
    return inner


@exclude_admin
def business_hours(request):
    business_days = BusinessHours.get_weekdays()
    blocks = BusinessHours.get_weekdays_blocks(business_days)
    business_opening = BusinessHours.get_opening_datetime(blocks)
    business_closing = BusinessHours.get_closing_datetime(blocks)
    return {
        'business_closing': business_closing,
        'business_days': business_days.items(),
        'business_opening': business_opening,
    }


@exclude_admin
def catalog_categories(request):
    return {
        'catalog_categories': Tag.objects.get_top_level(),
    }


@exclude_admin
def og_properties(request):
    return {
        'site_name': SITE_NAME,
        'page_title': SITE_NAME,
        'page_description': 'Malý čajový obchůdek v Mnichově Hradišti, \
který kromě čajů z celého světa prodává kávu, sušené ovoce \
v čokoládě nebo bez, bylinky, med, medoviny, porcelán a další.',
    }


@exclude_admin
def site_alerts(request):
    return {
        'site_alerts': SiteAlert.objects.get_active(),
    }
