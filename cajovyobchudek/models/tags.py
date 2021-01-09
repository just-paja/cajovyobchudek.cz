from django.utils.translation import gettext_lazy as _
from django.db.models import (
    CASCADE,
    BooleanField,
    ForeignKey,
    CharField,
    IntegerField,
    Model,
    TextField,
)


class Tag(Model):
    name = CharField(
        max_length=63,
        verbose_name=_('Name'),
    )
    description = TextField(
        null=True,
        blank=True,
        verbose_name=_('Description'),
    )
    public = BooleanField(
        default=True,
        verbose_name=_('Public'),
    )

    def __str__(self):
        return str(self.name)


class TagConnection(Model):
    parent = ForeignKey(
        Tag,
        on_delete=CASCADE,
        related_name='parent',
        verbose_name=_('Parent Tag'),
    )
    child = ForeignKey(
        Tag,
        on_delete=CASCADE,
        related_name='child',
        verbose_name=_('Child Tag'),
    )
    weight = IntegerField(
        default=0,
        verbose_name=('Child Weight'),
    )
