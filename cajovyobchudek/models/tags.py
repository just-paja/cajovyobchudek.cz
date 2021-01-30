from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.db.models import (
    CASCADE,
    ForeignKey,
    IntegerField,
    Manager,
    Model,
    SlugField,
)

from .fields import (
    NameField,
    DescriptionField,
    RenderedDescriptionField,
    VisibilityField
)


class TagManager(Manager):

    def public(self):
        return self.all().filter(public=True)

    def get_top_level(self):
        return self.public().filter(superiors=None)


class Tag(Model):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    name = NameField()
    slug = SlugField(
        max_length=63,
        unique=True,
    )
    description = DescriptionField(
        rendered_field='description_rendered',
    )
    description_rendered = RenderedDescriptionField()
    public = VisibilityField()
    objects = TagManager()

    def __str__(self):
        return str(self.name)

    @property
    def subordinate_tags(self):
        connections = self.subordinates.filter(
            subordinate__public=True
        ).order_by('weight').all()
        return [connection.subordinate for connection in connections]

    @property
    def descendants(self):
        subordinates = self.subordinate_tags
        result = [] + subordinates
        for tag in subordinates:
            result += tag.descendants
        return result

    @property
    def descendants_ids(self):
        return [tag.pk for tag in self.descendants]

    @property
    def product_tag_model(self):
        return apps.get_model(self._meta.app_label, 'ProductTag')

    @property
    def product_model(self):
        return apps.get_model(self._meta.app_label, 'Product')

    @property
    def products(self):
        ids = [self.pk] + self.descendants_ids
        return self.product_model.objects.filter(
            public=True,
            product_tags__pk__in=ids
        ).distinct()


class TagConnection(Model):

    class Meta:
        verbose_name = _('Tag Connection')
        verbose_name_plural = _('Tag Connections')

    superior = ForeignKey(
        Tag,
        on_delete=CASCADE,
        related_name='subordinates',
        verbose_name=_('Parent Tag'),
    )
    subordinate = ForeignKey(
        Tag,
        on_delete=CASCADE,
        related_name='superiors',
        verbose_name=_('Child Tag'),
    )
    weight = IntegerField(
        default=0,
        verbose_name=('Child Weight'),
    )

    def __str__(self):
        return str('%s > %s' % (self.superior.name, self.subordinate.name))
