from datetime import date

from django.utils import timezone

from config import celery_app
from order.reports import order_product_report


@celery_app.task
def order_product_report_task(from_date=None, end_date=None, send_mail=True):
    if end_date:
        end_date = date(*map(int, end_date.split("-")))
    else:
        end_date = timezone.now().date()
    if from_date:
        from_date = date(*map(int, from_date.split("-")))
        if from_date >= end_date:
            return "Invalid date"
    else:
        from_date = end_date - timezone.timedelta(days=7)
    instance = order_product_report(from_date, end_date)
    if instance and send_mail:
        pass  # TODO send email to admins
