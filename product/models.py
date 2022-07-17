from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError  # noqa
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config.base_models import TimeStampedModel
from product.managers import ProductDiscountQuerySet

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


class ProductDiscount(TimeStampedModel):
    objects = ProductDiscountQuerySet.as_manager()

    title = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField()
    rate = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(100)])

    class Meta:
        ordering = ['-start_at', '-end_at']
        verbose_name = _('Product discount')
        verbose_name_plural = _('Product discounts')

    def clean(self):
        if self.start_at >= self.end_at:
            raise ValidationError(
                {'start_at': _(
                    "The start time must be less than the end time")})

    def __str__(self):
        return self.title

    @property
    def is_active_now(self):
        now = timezone.now()
        return self.start_at <= now and self.end_at > now
