from django.urls import path

from .views import view_alerts, add_alerts, remove_alert

app_name = "alerts"
urlpatterns = [
    path("view_alerts/", view=view_alerts, name="view_alerts"),
    path("add_alerts/", view=add_alerts, name="add_alerts"),
    path("remove_alert/", view=remove_alert, name="remove_alert"),

]
