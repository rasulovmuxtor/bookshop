from django.db import models
from django.utils import timezone


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductDiscountQuerySet(models.QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(start_at__lte=now, end_at__gt=now)
