# -*- coding: utf-8 -*-
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