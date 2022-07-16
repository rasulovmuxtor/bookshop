from django.db.models import Avg
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from products.models import BookRating


@receiver(post_save, sender=BookRating)
def book_rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        """recalculate book rating after creation"""
        book_ratings = BookRating.objects.filter(book_id=instance.book_id)
        rating_avg = book_ratings.aggregate(Avg('rating'))['rating__avg']
        instance.book.rating = rating_avg
        instance.book.save(update_fields=['rating'])


@receiver(pre_delete, sender=BookRating)
def book_rating_pre_delete(sender, instance, *args, **kwargs):
    """recalculate book rating after deletion"""
    book_ratings = BookRating.objects.filter(book_id=instance.book_id)
    book_ratings = book_ratings.exclude(pk=instance.pk)
    rating_avg = book_ratings.aggregate(Avg('rating'))['rating__avg']
    instance.book.rating = rating_avg
    instance.book.save(update_fields=['rating'])
