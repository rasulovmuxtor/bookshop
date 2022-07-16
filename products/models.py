from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel

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


class Book(TimeStampedModel):
    author = models.ForeignKey(Author, models.PROTECT, 'books',
                               verbose_name=_('author'))
    category = models.ForeignKey(Category, models.PROTECT, 'books',
                                 verbose_name=_('category'))
    title = models.CharField(_("title"), max_length=128)
    slug = AutoSlugField(populate_from='title', editable=True,
                         unique=True, blank=True)
    description = RichTextField(_("description"))
    image = models.ImageField(_("image"), upload_to='books/images/')
    total_in_stock = models.PositiveIntegerField(_("total in stock"),
                                                 default=0)
    price = models.IntegerField(_("Price"))
    discount_price = models.IntegerField(_("discount price"), default=0)

    published_year = models.PositiveSmallIntegerField(
        _("published year"), validators=year_validators
    )
    rating = models.FloatField(
        _("rating"), null=True, editable=False, validators=rating_validators
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class BookRating(TimeStampedModel):
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_("user"))
    book = models.ForeignKey(Book, models.CASCADE, _("book"))
    rating = models.FloatField(_("rating"), validators=rating_validators)
    comment = models.TextField(_('comment'), blank=True)

    class Meta:
        verbose_name = _("Book Rating")
        verbose_name_plural = _("Book Rating")
        unique_together = ['user', 'book']
