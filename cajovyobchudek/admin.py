from django.contrib.admin import ModelAdmin, register, TabularInline
from django.utils.timezone import now

from . import models


@register(models.BusinessHours)
class BusinessHoursAdmin(ModelAdmin):
    list_display = ('weekday', 'from_hour', 'to_hour')


@register(models.ClosingRules)
class ClosingRulesAdmin(ModelAdmin):
    list_display = ('start', 'end', 'reason')


@register(models.SiteAlert)
class SiteAlertAdmin(ModelAdmin):
    list_display = ('name', 'is_visible', 'publish_at', 'hide_at')

    def is_visible(self, item):
        now_dt = now()
        return (
            (item.publish_at is None or item.publish_at <= now_dt) and
            (item.hide_at is None or now_dt <= item.hide_at)
        )


class TagConnection(TabularInline):
    model = models.TagConnection
    fk_name = 'superior'


@register(models.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'public')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        TagConnection,
    ]
