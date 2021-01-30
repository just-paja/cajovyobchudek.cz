from django.utils.translation import gettext_lazy as _
from django.db.models import (
    BooleanField,
    CASCADE,
    IntegerField,
    SlugField,
)
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from .fields import (
    NameField,
    DescriptionField,
    RenderedDescriptionField,
    VisibilityField
)


class TagManager(TreeManager):
    def get_top_level(self):
        return self.filter(public=True, main_menu=True)


class Tag(MPTTModel):

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    class MPTTMeta:
        order_insertion_by = ['weight', 'name']

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
    main_menu = BooleanField(
        default=False,
        verbose_name=_('Main menu'),
        help_text=_('Main menu items will appear in the page layout'),
    )
    parent = TreeForeignKey(
        'self',
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    weight = IntegerField(
        default=0,
        verbose_name=('Tag Weight'),
    )
    objects = TagManager()

    def __str__(self):
        return str(self.name)
