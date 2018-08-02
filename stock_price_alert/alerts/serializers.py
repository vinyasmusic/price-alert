from rest_framework import serializers
from stock_price_alert.users.models import User
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(slug_field='uuid', source='user',
                                           queryset=User.objects.all())

    class Meta:
        model = Alert
        fields = ('scrip_symbol', 'exchange_name', 'price', 'percentage', 'intraday_alert', 'user_id', 'uuid')
