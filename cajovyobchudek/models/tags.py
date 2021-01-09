from django.utils.translation import gettext_lazy as _
from django.db.models import (
    CASCADE,
    BooleanField,
    ForeignKey,
    CharField,
    IntegerField,
    Manager,
    Model,
    SlugField,
)

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class TagManager(Manager):

    def public(self):
        return self.all().filter(public=True)

    def get_top_level(self):
        return self.public().filter(superiors=None)


class Tag(Model):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    name = CharField(
        max_length=63,
        verbose_name=_('Name'),
    )
    slug = SlugField(
        max_length=63,
        unique=True,
    )
    description = MarkdownField(
        blank=True,
        null=True,
        rendered_field='description_rendered',
        validator=VALIDATOR_STANDARD,
        verbose_name=_('Description'),
    )
    description_rendered = RenderedMarkdownField(
        null=True,
        blank=True,
    )
    public = BooleanField(
        default=True,
        verbose_name=_('Public'),
    )
    objects = TagManager()

    def __str__(self):
        return str(self.name)

    @property
    def subordinate_tags(self):
        connections = self.subordinates.filter(subordinate__public=True).all()
        return [connection.subordinate for connection in connections]


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
