# -*- coding: utf-8 -*-
from djmoney.contrib.exchange.models import ExchangeBackend, Rate


class ExchangeManager():
    """
    Controller class for Default Exchange Rates operations
    """
    def __init__(self):
        # TODO refactor all FixedRates strings into settings' Variable
        self.backend_name = "FixedRates"
        self.exch_backnd, _ = ExchangeBackend.objects.get_or_create(name=self.backend_name, base_currency="USD")

    def set_rate(self, quote_currency, rate):
        rt, _ = Rate.objects.update_or_create(
            defaults={
                "value": rate
            },
            backend=self.exch_backnd,
            currency=quote_currency)
        return rt
