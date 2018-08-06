#### PRICEALERT.TRADE

This is a Django project where a user can setup alerts for stocks.

eg.
You can add alert for Apple (AAPL) listed on NASDAQ for a price of 200.7
with a tolerance percentage of 5%

We check for the set price every 6 hours and if that price is met at the
closing of the same or previous day then the system will send you an email.

Any suggestions or criticisms are welcome at users@pricealert.trade

Happy alerting !!


To-Do

- [ ] Add SMS support for non DND numbers
- [ ] Get a ssl certificate
- [ ] Write logic for intra-day check
- [ ] Add data about the scrip symbol in email
- [ ] Use IEX API for NASDAQ listed stocks
- [ ] Add support for Crypto alert
- [ ] Improve alerts add UI
- [ ] Try VueJS
- [ ] Use CI-CD

