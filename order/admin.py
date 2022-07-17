from django.contrib import admin

from order import models


@admin.register(models.CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    list_display = ['product_id', 'status', 'order_id', 'created_at']


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'type', 'created_at')
    list_filter = ('type',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
