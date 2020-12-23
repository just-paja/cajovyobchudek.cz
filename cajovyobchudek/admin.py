from django.contrib.admin import ModelAdmin, register

from . import models


@register(models.BusinessHours)
class BusinessHoursAdmin(ModelAdmin):
    list_display = ('weekday', 'from_hour', 'to_hour')


@register(models.ClosingRules)
class ClosingRulesAdmin(ModelAdmin):
    list_display = ('start', 'end', 'reason')
