import environ
import requests
import datetime
import time

from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from ..taskapp.celery import app
from alpha_vantage.timeseries import TimeSeries
from .models import Alert
from .serializers import AlertSerializer

logger = get_task_logger(__name__)
env = environ.Env()


def check_within_range(first_num, percent, second_num):
    decimal_percent = float(percent) / 200.0
    high_range = float(second_num) * (1.0 + decimal_percent)
    low_range = float(second_num) * (1.0 - decimal_percent)
    return low_range <= float(first_num) <= high_range


@app.task(bind=True)
def send_email_task(request):
    try:
        from_email = 'vinyasmusic@gmail.com'
        msg = EmailMultiAlternatives(subject='TEST', body='pppp', from_email='Price Alert <'+from_email+'>',
                                     to=['vinyasmusic@gmail.com'])
        msg.attach_alternative('Some text', "text/html")
        result = msg.send()
        print('RESULT ::::: {}'.format(result))
        print('RESULT ::::: {}'.format(msg.send))
        return True
    except Exception as e:
        print(e)
        return False


@app.task(bind=True)
def check_price(request):
    ts = TimeSeries(key=env('ALPHAVANTAGE_API_KEY'), output_format='json')
    today = datetime.datetime.now().date().isoformat()
    print(today)
    alerts = Alert.objects.filter(intraday_alert=False)
    for alert in alerts:
        data, meta_data = ts.get_daily(symbol=':'.join([alert.exchange_name, alert.scrip_symbol]))
        print('WHOLE DATA ::: {}'.format(data))
        price_data = data.get('2018-08-01', None)
        print('{} ::: {}'.format(alert.scrip_symbol, price_data))
        if price_data and alert.percentage:
            if check_within_range(price_data["4. close"], alert.percentage, alert.price):
                send_email_task()
        elif price_data and alert.price:
            if price_data["4. close"] == alert.price:
                send_email_task()
        time.sleep(4)


@app.task(bind=True)
def send_simple_message(request):
    mailgun_key = env('MAILGUN_KEY')

    return requests.post(
        "https://api.mailgun.net/v3/sandbox8c267a01d8974690ae2c644631fc31da.mailgun.org/messages",
        auth=("api", mailgun_key),
        data={"from": "Excited User <mailgun@mailgun.org>",
              "to": ["vinyasmusic@gmail.com", "vinyasofficial@gmail.com", "vinyas@reckonsys.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})
