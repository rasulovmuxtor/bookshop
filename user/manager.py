from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Note: username as a phone_number
        Create and save a user with the given phone_number, email, and password
        """
        phone_number = username
        if not phone_number:
            raise ValueError('The given phone must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(phone_number=phone_number, email=email,
                          **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **kwargs):  # noqa
        return super(CustomUserManager, self).create_user(phone_number, email, password, **kwargs)  # noqa

    def create_superuser(self, phone_number, email=None, password=None, **kwargs):  # noqa
        return super(CustomUserManager, self).create_superuser(phone_number, email, password, **kwargs)  # noqa
