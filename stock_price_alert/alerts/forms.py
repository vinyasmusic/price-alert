import random
from django.contrib.auth import get_user_model
from django.forms import ModelForm, CharField, BooleanField, FloatField, Form
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Field
from crispy_forms.bootstrap import Accordion, AccordionGroup, Tab, TabHolder, FormActions

User = get_user_model()


class AlertFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AlertFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        r = random.randint(1, 100)
        self.layout = Layout(
            Accordion(

                Fieldset('Alert Data', 'scrip_symbol', 'exchange_name', 'price', 'percentage',
                         'intraday_alert')

            )
        )


class AlertForm(Form):
    scrip_symbol = CharField(max_length=50,
                             widget=TextInput(attrs={'placeholder': 'Scrip symbol like GOOGL'}))
    exchange_name = CharField(max_length=10,
                              widget=TextInput(attrs={'placeholder': 'Exchange names like NSE or BSE'}))
    price = FloatField(widget=TextInput(attrs={'placeholder': 'Price of the scrip at which you want alert'}))
    percentage = FloatField(required=False,
                            widget=TextInput(attrs={'placeholder': 'Notify on what % drop after alert price'}))
    intraday_alert = BooleanField(required=False)


class ExampleForm(Form):
    favorite_color = CharField(max_length=50)
    favorite_food = CharField(max_length=50)


class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Accordion(
            AccordionGroup('First Group', Field('favorite_color'), Field('favorite_food'), active=False
                           ),
            AccordionGroup('Second Group', Field('favorite_color'), Field('favorite_food'), active=True

                           )
        )
        self.render_required_fields = True
