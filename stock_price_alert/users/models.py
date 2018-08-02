import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    phone_number = PhoneNumberField(blank=True)
    address = CharField(_("Address of User"), blank=True, max_length=255)
    uuid = UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
