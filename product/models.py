from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError  # noqa
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.base_models import TimeStampedModel

User = get_user_model()
year_validators = [MinValueValidator(1900), MaxValueValidator(2099)]
rating_validators = [MinValueValidator(1), MaxValueValidator(5)]


class Category(TimeStampedModel):
    title = models.CharField(_("title"), max_length=128)
    slug = AutoSlugField(populate_from='title', editable=True,
                         unique=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title']

    def __str__(self):
        return self.title


class Author(TimeStampedModel):
    full_name = models.CharField(_("full name"), max_length=128)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Product(TimeStampedModel):
    """Book model"""
    author = models.ForeignKey(Author, models.PROTECT, 'products',
                               verbose_name=_('author'))
    category = models.ForeignKey(Category, models.PROTECT, 'products',
                                 verbose_name=_('category'))
    title = models.CharField(_("title"), max_length=128)
    slug = AutoSlugField(populate_from='title', editable=True,
                         unique=True, blank=True)
    description = RichTextField(_("description"))
    image = models.ImageField(_("image"), upload_to='products/images/')
    total_in_stock = models.PositiveIntegerField(_("total in stock"),
                                                 default=0, editable=False)
    total_sold = models.PositiveIntegerField(_("total sold"),
                                             default=0, editable=False)
    price = models.IntegerField(_("Price"))
    discount_price = models.IntegerField(_("discount price"), default=0)

    published_year = models.PositiveSmallIntegerField(
        _("published year"), validators=year_validators, null=True, blank=True
    )
    rating = models.FloatField(
        _("rating"), null=True, editable=False, validators=rating_validators
    )
    is_active = models.BooleanField(
        help_text=_('Designates whether the client can see this product'))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductEntry(TimeStampedModel):
    user = models.ForeignKey(User, models.PROTECT, null=True, editable=False)
    product = models.ForeignKey(Product, models.CASCADE)
    comment = models.TextField(blank=True)
    quantity = models.IntegerField(_("Quantity"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Product Entry")
        verbose_name_plural = _("Product Entry")

    def clean(self):
        if self.quantity == 0:
            raise ValidationError({'quantity': _("this field can not be 0")})

    def __str__(self):
        return str(self.quantity)


class ProductRating(TimeStampedModel):
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_("user"))
    product = models.ForeignKey(Product, models.CASCADE, _("product"))
    rating = models.FloatField(_("rating"), validators=rating_validators)
    comment = models.TextField(_('comment'), blank=True)

    class Meta:
        verbose_name = _("Product Rating")
        verbose_name_plural = _("Product Ratings")
        unique_together = ['user', 'product']
