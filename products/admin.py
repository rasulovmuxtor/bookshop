from django.contrib import admin
from products import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price',
                    'total_in_stock', 'modified_at']
    search_fields = ['title', 'author__full_name']
    list_filter = ['category']
    readonly_fields = ['rating']
    autocomplete_fields = ['author', 'category']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'modified_at']
    search_fields = ['title']


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'modified_at']
    search_fields = ['full_name']
