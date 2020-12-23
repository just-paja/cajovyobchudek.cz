from cajovyobchudek.models import BusinessHours


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