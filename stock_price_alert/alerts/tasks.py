import environ
import datetime
import time
import logging
import pytz
import pprint
from django.conf import LazySettings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ..taskapp.celery import app
from alpha_vantage.timeseries import TimeSeries
import nsetools
from .models import Alert

logging.basicConfig(filename='tasks.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger(__name__)
env = environ.Env()
settings = LazySettings()


def check_within_range(first_num, percent, second_num):
    decimal_percent = float(percent) / 200.0
    high_range = float(second_num) * (1.0 + decimal_percent)
    low_range = float(second_num) * (1.0 - decimal_percent)
    return low_range <= float(first_num) <= high_range


@app.task(bind=True)
def send_email_task(request, to_email,
                    scrip_symbol, price, percentage=None, today=datetime.datetime.now().date(), data=None):
    try:
        from_email = settings.EMAIL_ID

        if percentage:
            html_content = render_to_string('mail_template.html', data)
        else:
            html_content = render_to_string('mail_template.html', data)
            # render with dynamic value

        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
        msg = EmailMultiAlternatives(subject='[IMP] Price Alert for {}'.format(scrip_symbol),
                                     body=text_content,
                                     from_email='Price Alert <' + from_email + '>',
                                     to=[to_email])
        msg.attach_alternative(html_content, "text/html")
        result = msg.send()
        return True
    except Exception as e:
        logging.exception(e)
        return False


def get_today():
    today = datetime.datetime.now().date()
    if today.isoweekday() <= 5:
        today = today.isoformat()
    else:
        today = datetime.datetime.now().date().replace(day=datetime.datetime.now().date().day - 2).isoformat()
    return today


def get_nasdaq_data_and_check(alert):
    ts = TimeSeries(key=env('ALPHAVANTAGE_API_KEY'), output_format='json')
    today = get_today()
    data, meta_data = ts.get_daily(symbol=':'.join([alert.exchange_name.strip(), alert.scrip_symbol.strip()]))
    try:
        price_data = data[today]
    except Exception as e:
        log.exception(e)
        price_data = data.get(datetime.datetime.now(pytz.timezone('US/Eastern')).date().isoformat(), None)
    if price_data and alert.percentage:
        if check_within_range(price_data["4. close"], alert.percentage, alert.price):
            return True, price_data

    elif price_data and alert.price:
        if float(price_data["4. close"]) <= float(alert.price):
            return True, price_data
    return False, {}


def get_nse_data_and_check(alert):
    nse = nsetools.Nse()
    if nse.is_valid_code(alert.scrip_symbol):
        quote = nse.get_quote(alert.scrip_symbol)
        if alert.percentage:
            if check_within_range(quote['closePrice'],
                                  alert.percentage,
                                  alert.price) or \
                check_within_range(quote['lastPrice'],
                                   alert.percentage,
                                   alert.price):
                return True, quote
        elif float(quote['closePrice']) <= alert.price or float(quote['lastPrice']) <= alert.price:
            return True, quote

    return False, {}


@app.task(bind=True)
def check_price(request):
    alerts = Alert.objects.filter(intraday_alert=False)
    today = get_today()

    for alert in alerts:
        check = False
        data = {}
        if alert.exchange_name.strip().lower() == 'nasdaq':
            check, data = get_nasdaq_data_and_check(alert)
        elif alert.exchange_name.strip().lower() == 'nse':
            check, data = get_nse_data_and_check(alert)

        context = {'scrip_symbol': alert.scrip_symbol.strip(),
                   'price': alert.price,
                   'percentage': alert.percentage,
                   'site': 'https://pricealert.trade',
                   'date': today
                   }
        if len(data) > 0:
            # Find out why the data.get('1. open', data['open']) is giving error
            try:
                context['open'] = data.get('1. open', 'NA')
                context['close'] = data.get('4. close', 'NA')
                context['high'] = data.get('2. high', 'NA')
                context['low'] = data.get('3. low', 'NA')
                context['traded_volume'] = data.get('5. volume', 'NA')
                context['total_buy'] = data.get('totalBuyQuantity', 'NA')
                context['total_sell'] = data.get('totalSellQuantity', 'NA')
                context['week_low'] = data.get('low52', 'NA')
                context['week_high'] = data.get('high52', 'NA')
            except KeyError:
                context['open'] = data.get('1. open', data['open'])
                context['close'] = data.get('4. close', data['closePrice'])
                context['high'] = data.get('2. high', data['dayHigh'])
                context['low'] = data.get('3. low', data['dayLow'])
                context['traded_volume'] = data.get('5. volume', data['totalTradedVolume'])
                context['total_buy'] = data.get('totalBuyQuantity', 'NA')
                context['total_sell'] = data.get('totalSellQuantity', 'NA')
                context['week_low'] = data.get('low52', 'NA')
                context['week_high'] = data.get('high52', 'NA')

        if check and alert.percentage:
            send_email_task(to_email=alert.user.email, scrip_symbol=alert.scrip_symbol,
                            price=alert.price, percentage=alert.percentage,
                            today=today, data=context)
        elif check:
            send_email_task(to_email=alert.user.email, scrip_symbol=alert.scrip_symbol,
                            price=alert.price, today=today, data=context)

        time.sleep(20)
