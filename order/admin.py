from django.contrib import admin

from order import models


@admin.register(models.CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    pass
