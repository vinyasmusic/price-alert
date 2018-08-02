from django.contrib import admin
from .models import Alert


class AlertAdmin(admin.ModelAdmin):

    list_display = ['scrip_symbol', 'exchange_name', 'price', 'percentage', 'intraday_alert']
    list_filter = ['scrip_symbol', 'exchange_name']
    search_fields = ['scrip_symbol', 'exchange_name']


admin.site.register(Alert, AlertAdmin)
