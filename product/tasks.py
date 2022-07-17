import json

from django.db.models import F
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from config import celery_app
from product.models import ProductDiscount


@celery_app.task
def task_product_discount(pk: int, is_start=True):
    instance = ProductDiscount.objects.get(pk=pk)

    if is_start:
        rate = 1 - instance.rate / 100
        instance.products.update(discount_price=F('price') * rate)

        clocked = ClockedSchedule.objects.create(clocked_time=instance.end_at)
        args = json.dumps([instance.pk, False])
        PeriodicTask.objects.create(
            one_off=True,
            clocked=clocked,
            name=f'Product-Discount-End-{instance.pk}',
            task='product.tasks.task_product_discount',
            args=args,
            description=instance.title
        )
    else:
        instance.products.update(discount_price=0)
