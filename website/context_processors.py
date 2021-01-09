from cajovyobchudek.models import BusinessHours, SiteAlert, Tag


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


def catalog_categories(request):
    return {
        'catalog_categories': Tag.objects.get_top_level(),
    }


def og_properties(request):
    return {
        'site_name': 'Čaje z celého světa',
        'page_title': 'Čaje z celého světa',
        'page_description': 'Malý čajový obchůdek v Mnichově Hradišti, \
který kromě čajů z celého světa prodává kávu, sušené ovoce \
v čokoládě nebo bez, bylinky, med, medoviny, porcelán a další.',
    }


def site_alerts(request):
    alerts = SiteAlert.objects.get_active()
    return {
        'site_alerts': alerts,
    }
