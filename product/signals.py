from django.db.models import Avg
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from product.models import ProductEntry, ProductRating


@receiver(post_save, sender=ProductRating)
def product_rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        """recalculate product rating after creation"""
        ratings = ProductRating.objects.filter(book_id=instance.book_id)
        rating_avg = ratings.aggregate(Avg('rating'))['rating__avg']
        instance.product.rating = rating_avg
        instance.product.save(update_fields=['rating'])


@receiver(pre_delete, sender=ProductRating)
def product_rating_pre_delete(sender, instance, *args, **kwargs):
    """recalculate product rating after deletion"""
    ratings = ProductRating.objects.filter(product_id=instance.product_id)
    ratings = ratings.exclude(pk=instance.pk)
    rating_avg = ratings.aggregate(Avg('rating'))['rating__avg']
    instance.product.rating = rating_avg
    instance.product.save(update_fields=['rating'])


@receiver(post_save, sender=ProductEntry)
def product_entry_post_save(sender, instance, created, *args, **kwargs):
    if created:
        """recalculate product total_in_stock after creation"""
        instance.product.total_in_stock = instance.quantity
        instance.product.save(update_fields=['total_in_stock'])
