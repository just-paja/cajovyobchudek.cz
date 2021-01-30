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


class TagConnectionAdmin(TabularInline):
    model = models.TagConnection
    fk_name = 'superior'
    extra = 0


@register(models.Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name',)


class ProductTagAdmin(TabularInline):
    model = models.ProductTag
    extra = 0


class ProductPhotoAdmin(TabularInline):
    model = models.ProductPhoto
    extra = 0


@register(models.ProductDescription)
class ProductDescriptionAdmin(ModelAdmin):
    pass


@register(models.ProductUsage)
class ProductUsageAdmin(ModelAdmin):
    pass


@register(models.Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'local_name', 'product_code', 'public', 'producer')
    inlines = (ProductTagAdmin, ProductPhotoAdmin,)


@register(models.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'public')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        TagConnectionAdmin,
        ProductTagAdmin,
    ]
