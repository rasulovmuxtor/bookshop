from django.utils import timezone

from config import celery_app
from order.reports import weekly_order_product_report


@celery_app.task(time_limit=1500, soft_time_limit=1000)
def mail_weekly_report():
    instance = weekly_order_product_report(timezone.now().date())
    if instance:
        pass  # TODO send email to admins
