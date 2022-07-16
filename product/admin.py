from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from product import models


class ProductEntryInline(TabularInlinePaginated):
    fields = ('quantity', 'user', 'created_at')
    readonly_fields = ('user', 'created_at')
    per_page = 3
    model = models.ProductEntry
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.Product)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price',
                    'total_in_stock', 'modified_at')
    search_fields = ('title', 'author__full_name')
    list_filter = ('category',)
    readonly_fields = ('total_in_stock', 'rating', 'total_sold')
    autocomplete_fields = ('author', 'category')
    inlines = (ProductEntryInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category')

    def save_formset(self, request, form, formset, change):
        for inline_form in formset.forms:
            if inline_form.has_changed():
                inline_form.instance.user = request.user
        super().save_formset(request, form, formset, change)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'modified_at')
    search_fields = ('title',)


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'modified_at')
    search_fields = ('full_name',)
