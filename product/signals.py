import json

from django.db.models import Avg
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from product.models import ProductDiscount, ProductEntry, ProductRating
from product.tasks import task_product_discount


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


@receiver(post_save, sender=ProductDiscount)
def product_discount_post_save(sender, instance, created, *args, **kwargs):
    """Create tasks to apply discounts"""
    if created:
        if instance.is_active_now:
            task_product_discount.apply_async(args=[instance.pk, True],
                                              countdown=2)
        else:
            now = timezone.now() + timezone.timedelta(seconds=2)
            time = now if instance.start_at < now else instance.start_at
            clocked = ClockedSchedule.objects.create(clocked_time=time)
            args = json.dumps([instance.pk, True])
            PeriodicTask.objects.create(
                one_off=True,
                clocked=clocked,
                name=f'Product-Discount-Start-{instance.pk}',
                task='product.tasks.task_product_discount',
                args=args,
                description=instance.title
            )
    # TODO implement period change cases
