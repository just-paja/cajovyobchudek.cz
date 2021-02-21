from django.utils.translation import gettext_lazy as _
from django.db.models import (
    ImageField,
    IntegerField,
    ForeignKey,
    Model,
    Manager,
    ManyToManyField,
    RESTRICT,
    CASCADE,
    PositiveIntegerField,
    SlugField,
)

from .fields import (
    DescriptionField,
    FaculativeForeignKey,
    NameField,
    RenderedDescriptionField,
    VisibilityField,
)


class ProductManager(Manager):

    def public(self):
        return self.all().filter(public=True)


class Product(Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = NameField(
        verbose_name=_('Product Name'),
        help_text=_('Define the original product name, for example "Yu Guan Yin"'),
    )
    local_name = NameField(
        verbose_name=_('Localized Name'),
        help_text=_('Define the localized name, for example "Nefritová Bohyně Milosrdenství"'),
    )
    slug = SlugField(
        max_length=127,
        unique=True,
    )
    public = VisibilityField()
    producer = FaculativeForeignKey(
        'Company',
        help_text=_('Product maker, creator, author'),
        related_name='produced_items',
        verbose_name=_('Producer'),
    )
    product_code = PositiveIntegerField(
        verbose_name=_('Product Code'),
        blank=True,
        null=True,
        help_text=_('Product number, barcode number')
    )
    distributor = FaculativeForeignKey(
        'Company',
        help_text=_('Product maker, creator, author'),
        related_name='distributed_items',
        verbose_name=_('Distributor'),
    )

    description = FaculativeForeignKey(
        'ProductDescription',
        on_delete=RESTRICT,
        verbose_name=_('Description'),
    )
    usage = FaculativeForeignKey(
        'ProductUsage',
        on_delete=RESTRICT,
        verbose_name=_('Usage'),
    )
    variants = ManyToManyField('self')
    objects = ProductManager()

    def __str__(self):
        return str(self.name)


class ProductLink(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'Product'
        kwargs['on_delete'] = CASCADE
        kwargs['verbose_name'] = _('Product')
        super().__init__(*args, **kwargs)


class ProductTag(Model):
    product = ProductLink(
        related_name='product_tags'
    )
    tag = ForeignKey(
        'Tag',
        on_delete=RESTRICT,
        related_name='product_tags',
        verbose_name=_('Tag'),
    )
    weight = IntegerField(
        default=0,
        verbose_name=('Product Weight'),
    )

    def __str__(self):
        return '%s - %s' % (self.product, self.tag)


class ProductPhoto(Model):
    product = ProductLink(
        related_name='photos'
    )
    photo = ImageField(
        verbose_name=_('Photo'),
    )


class ProductNarrative(Model):
    class Meta:
        abstract = True

    name = NameField()
    text = DescriptionField(
        rendered_field='text_rendered',
    )
    text_rendered = RenderedDescriptionField()

    def __str__(self):
        return str(self.pk)


class ProductDescription(ProductNarrative):
    class Meta:
        verbose_name = _('Product Description')
        verbose_name_plural = _('Product Descriptions')


class ProductUsage(ProductNarrative):
    class Meta:
        verbose_name = _('Product Usage')
        verbose_name_plural = _('Product Usages')
