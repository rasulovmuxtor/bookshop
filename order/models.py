from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.base_models import TimeStampedModel

User = get_user_model()


class CartProduct(TimeStampedModel):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey('product.Product', models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['-modified_at']
        unique_together = ['user', 'product']
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name="quantity must be greater or equal to 0",
            )
        ]


class OrderStatus(models.TextChoices):
    canceled = 'canceled', _("Canceled")
    verifying = 'verifying', _("Verifying")
    verified = 'verified', _("verified")
    on_the_way = 'on_the_way', _("On the Way")
    delivered = 'delivered', _("Delivered")


class PaymentType(models.TextChoices):
    cash = 'cash', _("Cash")


class PaymentStatus(models.TextChoices):
    unpaid = 'unpaid', _("Unpaid")
    paid = 'paid', _("Paid")


class Order(TimeStampedModel):
    user = models.ForeignKey(User, models.CASCADE, related_name='orders')
    status = models.CharField(max_length=32, choices=OrderStatus.choices,
                              default=OrderStatus.verifying)

    # PAYMENT
    payment_status = models.CharField(max_length=32,
                                      choices=PaymentStatus.choices,
                                      default=PaymentStatus.unpaid)
    payment_type = models.CharField(max_length=32, choices=PaymentType.choices)
    # address
    address = models.CharField(max_length=256)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    delivery_price = models.IntegerField()
    total_price = models.IntegerField()
    order_price = models.IntegerField()

    class Meta:
        ordering = ['-id']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    @staticmethod
    def get_delivery_price():
        # TODO return static price or calculated price by distance
        return 0

    def get_order_price(self):
        return self.delivery_price + self.total_price


class OrderProductStatus(models.TextChoices):
    canceled = 'canceled', _("canceled")
    verifying = 'verifying', _("verifying")
    verified = 'verified', _("verified")


class OrderProduct(TimeStampedModel):
    product = models.ForeignKey('product.Product', models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    comment = models.TextField(blank=True)

    order = models.ForeignKey(Order, models.CASCADE,
                              related_name='order_products')
    status = models.CharField(max_length=32,
                              choices=OrderProductStatus.choices,
                              default=OrderProductStatus.verifying)

    class Meta:
        ordering = ['order']
        unique_together = ['order', 'product']
        verbose_name = _("Order Product")
        verbose_name_plural = _("Order Products")

    @property
    def total_price(self):
        return self.price * self.quantity


class ReportType(models.TextChoices):
    weekly_order_product = 'weekly_order_product', _("weekly order product")
    custom = 'custom', _("custom")


class Report(TimeStampedModel):
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=32, choices=ReportType.choices)
    document = models.FileField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
