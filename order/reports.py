import os
from datetime import timedelta

from django.conf import settings
from django.db.models import Sum

from order.models import OrderStatus  # noqa
from order.models import OrderProduct, OrderProductStatus, Report, ReportType
from order.workbooks import BaseWorkbook


def weekly_order_product_report(date):
    last_week = date - timedelta(days=6)
    queryset = OrderProduct.objects.filter(
        status=OrderProductStatus.verified,
        created_at__date__gte=last_week, created_at__date__lte=date,
        order__status=OrderStatus.verified
    )
    queryset = queryset.values('product_id').annotate(total=Sum('quantity'))
    queryset = queryset.order_by('product_id').values_list('product__title',
                                                           'total')
    if not queryset:
        return None
    title = f'{last_week}-{date}'
    wb = BaseWorkbook()
    sheet = wb.add_sheet('report')
    sheet.col(0).width = wb.short_width
    sheet.col(1).width = wb.long_width
    sheet.col(2).width = wb.middle_width
    sheet.col(3).width = wb.middle_width
    sheet.col(4).width = wb.middle_width
    sheet.row(0).height = wb.tall_height

    sheet.write_merge(0, 0, 1, 3, title, wb.h_bold_center)
    sheet.write(1, 0, "№", wb.bold_left)
    sheet.write(1, 1, "Products", wb.bold_center)
    sheet.write(1, 2, "Total sold", wb.bold_center)

    for row, val in enumerate(queryset, 2):
        sheet.write(row, 0, row - 1)
        sheet.write(row, 1, val[0])
        sheet.write(row, 2, val[1])
    filename = f"{title}.xls"
    directory = f"{settings.MEDIA_ROOT}/reports/weekly"
    file_dir_exists = os.path.exists(directory)
    if not file_dir_exists:
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    wb.save(filepath)
    instance = Report(date=date, type=ReportType.weekly_order_product)
    instance.document.name = f"reports/weekly/{filename}"
    instance.save()
    return instance
