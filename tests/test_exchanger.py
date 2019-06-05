# -*- coding: utf-8 -*-
import unittest
################# Universal Import ###################################################
import sys
import os
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SELF_DIR)
PREROOT_DIR = os.path.dirname(ROOT_DIR)
print(ROOT_DIR)
sys.path.append(ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_simple_payment_system.settings")
# #####################################################
import django

django.setup()
from djmoney.money import Money, Currency
from djmoney.contrib.exchange.models import ExchangeBackend, Rate
from djmoney.contrib.exchange.models import convert_money
from djmoney.contrib.exchange.models import get_rate


class CurrencyExchangerTest(unittest.TestCase):
    def setUp(self):
        self.backend_name = "FixedRates"
        eb, _ = ExchangeBackend.objects.get_or_create(name=self.backend_name, base_currency="USD")
        #cad_rate = Rate(backend=eb, currency="CAD", value=1.26)
        #cny_rate = Rate(backend=eb, currency="CNY", value=6.9)
        #eur_rate = Rate(backend=eb, currency="EUR", value=0.89)

    def test_rates(self):
        rate = get_rate('USD', 'EUR', backend=self.backend_name)
        print(rate)
        #from decimal import Decimal
        self.assertEqual(float(rate), 0.89)

    def test_converter(self):
        converted_value = convert_money(Money(100, 'EUR'), 'USD')
        print(converted_value)
        self.assertEqual(converted_value.currency, Currency('USD'))
        #print(converted_value.__dict__)
        self.assertEqual(float(converted_value.amount), 100.0/0.89)

    def test_converter_2step(self):
        converted_value = convert_money(Money(100, 'EUR'), 'CNY')
        print(converted_value)
        self.assertEqual(converted_value.currency, Currency('CNY'))
        self.assertEqual(float(converted_value.amount), 100.0/0.89*6.9)

if __name__ == "__main__":
    unittest.main()