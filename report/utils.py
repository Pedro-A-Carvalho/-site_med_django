import datetime
import decimal
import json
from django.utils.translation import gettext as _
from .models import ReportDefinition


def create_base_report_template(report_type):
    # use a predefined report definition so you don't have to start from scratch in this demo app,
    # for a real word app you would probably start with an empty report if nothing was saved previously

    report_definition = ''

    ReportDefinition.objects.create(
        report_type=report_type, report_definition=json.dumps(report_definition),
        last_modified_at=datetime.datetime.now())


def json_default(obj):
    """Serializes decimal and date values, can be used for json encoder."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.date):
        return str(obj)
    raise TypeError
