import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from stock_price_alert.users.models import User


class Alert(TimeStampedModel):
    scrip_symbol = models.CharField(max_length=50)
    exchange_name = models.CharField(max_length=10)
    price = models.FloatField()
    percentage = models.FloatField(blank=True, null=True)
    intraday_alert = models.BooleanField(default=False, help_text='Set if you want to check intraday prices')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

