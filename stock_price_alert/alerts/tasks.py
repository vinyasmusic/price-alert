import environ
import requests
import datetime
import time
import logging

from django.core.mail import EmailMultiAlternatives
from ..taskapp.celery import app
from alpha_vantage.timeseries import TimeSeries
from .models import Alert

logging.basicConfig(filename='tasks.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger(__name__)
env = environ.Env()


def check_within_range(first_num, percent, second_num):
    decimal_percent = float(percent) / 200.0
    high_range = float(second_num) * (1.0 + decimal_percent)
    low_range = float(second_num) * (1.0 - decimal_percent)
    return low_range <= float(first_num) <= high_range


@app.task(bind=True)
def send_email_task(request, to_email,
                    scrip_symbol, price, percentage=None, today=datetime.datetime.now().date()):
    try:
        from_email = 'vinyasmusic@gmail.com'
        if percentage:

            body = 'Your price of {} with a tolerance of {} % for {} has been hit on {}.'.format(price,
                                                                                                 percentage,
                                                                                                 scrip_symbol,
                                                                                                 today)
        else:
            body = 'Your price of {} for {} has been hit on {}.'.format(price,
                                                                        scrip_symbol,
                                                                        today)
        msg = EmailMultiAlternatives(subject='[IMP] Price Alert for {}'.format(scrip_symbol),
                                     body=body,
                                     from_email='Price Alert <'+from_email+'>',
                                     to=[to_email])
        msg.attach_alternative('', "text/html")
        result = msg.send()
        return True
    except Exception as e:
        logging.exception(e)
        return False


@app.task(bind=True)
def check_price(request):
    ts = TimeSeries(key=env('ALPHAVANTAGE_API_KEY'), output_format='json')
    today = datetime.datetime.now().date().isoformat()
    alerts = Alert.objects.filter(intraday_alert=False)
    for alert in alerts:
        data, meta_data = ts.get_daily(symbol=':'.join([alert.exchange_name, alert.scrip_symbol]))
        price_data = data.get(today, datetime.datetime.now().date().replace(day=datetime.datetime.now().date().day-2))

        if price_data and alert.percentage:
            if check_within_range(price_data["4. close"], alert.percentage, alert.price):
                send_email_task(to_email=alert.user.email, scrip_symbol=alert.scrip_symbol,
                                price=alert.price, percentage=alert.percentage,
                                today=today)

        elif price_data and alert.price:
            if price_data["4. close"] == alert.price:

                send_email_task(to_email=alert.user.email, scrip_symbol=alert.scrip_symbol,
                                price=alert.price, today=today)
        time.sleep(4)


@app.task(bind=True)
def send_simple_message(request):
    mailgun_key = env('MAILGUN_KEY')
    response = requests.post(
        "https://api.mailgun.net/v3/pricealert.trade/messages",
        auth=("api", mailgun_key),
        data={"from": "Excited User <alert@pricealert.trade>",
              "to": ["vinyasmusic@gmail.com", "vinyasofficial@gmail.com", "vinyas@reckonsys.com",
                     "susantamcacvrca@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

    return response.text
