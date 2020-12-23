from django.contrib.admin import ModelAdmin, register

from .models import BusinessHours


@register(BusinessHours)
class BusinessHoursAdmin(ModelAdmin):
    list_display = ('weekday', 'from_hour', 'to_hour')
