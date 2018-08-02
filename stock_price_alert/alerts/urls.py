from django.urls import path

from .views import view_alerts, add_alerts

app_name = "alerts"
urlpatterns = [
    path("view_alerts/", view=view_alerts, name="set_alerts"),
    path("add_alerts/", view=add_alerts, name="add_alerts"),

]
