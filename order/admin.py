from django.contrib import admin
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from order import models


class OrderProductInline(admin.TabularInline):
    extra = 0
    model = models.OrderProduct
    autocomplete_fields = ('product',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'phone_number', 'status', 'payment_status', 'order_price',
        'created_at'
    )
    autocomplete_fields = ('user',)
    inlines = (OrderProductInline,)

    def phone_number(self, obj):
        return obj.phone_number

    phone_number.short_description = _("user")  # type: ignore

    def get_queryset(self, request):
        queryset = super(OrderAdmin, self).get_queryset(request)
        return queryset.annotate(phone_number=F('user__phone_number'))


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_title', 'order_id', 'status', 'created_at']

    def product_title(self, obj):
        return obj.product_title

    product_title.short_description = _("title")  # type: ignore

    def get_queryset(self, request):
        queryset = super(OrderProductAdmin, self).get_queryset(request)
        return queryset.annotate(product_title=F('product__title'))


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('title',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
