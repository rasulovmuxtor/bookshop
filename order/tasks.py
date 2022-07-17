from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from config import celery_app
from order.reports import order_product_report

User = get_user_model()


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
        emails = User.get_admin_email_list()
        if not emails:
            return
        try:
            link = f'{settings.HOST}{instance.document.url}'
            body = "<b>Report {}.<b> <br> <a href={}>Download</a>".format(
                instance.title,
                link
            )
            message = EmailMultiAlternatives('Report')
            message.to = emails
            message.alternatives = ((body, 'text/html'),)
            message.attach_file(path=instance.document.path)
            message.send()
        except Exception as e:
            print(e)
            return "Failed to send email"
