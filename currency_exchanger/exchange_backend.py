# -*- coding: utf-8 -*-
import json
from decimal import Decimal

from django.db.transaction import atomic
from django.utils.http import urlencode

from djmoney import settings
from djmoney._compat import parse_qsl, urlopen, urlparse, urlunparse

from djmoney.contrib.exchange.models import ExchangeBackend, Rate
from djmoney.contrib.exchange.backends.base import BaseExchangeBackend


class FixedRatesExchangeBackend(BaseExchangeBackend):
    """
    Backend for updating currencies from HTTP API
    """
    name = "FixedRates"
    url = None

    def get_rates(self, **kwargs):
        """
        Returns a mapping <currency>: <rate>.
        """
        print("get_rates!!!")
        raise NotImplementedError

    def get_url(self, **params):
        """
        Updates base url with provided GET parameters.
        """
        print("get_url")
        parts = list(urlparse(self.url))
        query = dict(parse_qsl(parts[4]))
        query.update(params)
        parts[4] = urlencode(query)
        return urlunparse(parts)

    def get_params(self):
        """
        Default GET parameters for the request.
        """
        print("get_params")
        return {}

    def get_response(self, **params):
        print("get_response")
        url = self.get_url(**params)
        #response = urlopen(url, cafile=certifi.where())
        #return response.read()

    def parse_json(self, response):
        print("parse_json")
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        return json.loads(response, parse_float=Decimal)

    @atomic
    def update_rates(self, base_currency=settings.BASE_CURRENCY, **kwargs):
        """
        Updates rates for the given backend.
        """
        print("update_rates")
        backend, _ = ExchangeBackend.objects.update_or_create(name=self.name, defaults={"base_currency": base_currency})
        backend.clear_rates()
        params = self.get_params()
        params.update(base_currency=base_currency, **kwargs)
        Rate.objects.bulk_create(
            [
                Rate(currency=currency, value=value, backend=backend)
                for currency, value in self.get_rates(**params).items()
            ]
        )
from djmoney.contrib.exchange.models import get_default_backend_name, get_rate
print("get_default_backend_name()")
print(get_default_backend_name())