from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel

from .manager import CustomUserManager

phone_validators = [RegexValidator(
    regex=r"^\+{1}998\d{9}$",
    message=_(
        "Phone number must be entered in the format: '+998991234567'.",
    ),
)]


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'

    phone_number = models.CharField(_("phone number"), max_length=13,  # noqa
                                    validators=phone_validators, unique=True,  # noqa
                                    error_messages={
                                        "unique": _("A user with that phone number already exists.")})  # noqa

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    address = models.CharField(_("address"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site")
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class SMSVerification(TimeStampedModel):
    security_code = models.CharField(_("security Code"), max_length=6)
    phone_number = models.CharField(_("phone number"), max_length=13,
                                    validators=phone_validators)
    is_verified = models.BooleanField(_("verified"), default=False)

    class Meta:
        verbose_name = _("SMS Verification")
        verbose_name_plural = _("SMS Verifications")
        ordering = ("-modified_at",)
        unique_together = ("security_code", "phone_number")

    def __str__(self):
        return f"{self.phone_number}: {self.security_code}"
