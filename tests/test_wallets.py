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

from wallets.models import Wallet, FillUpBroker, TransferTransaction, FillUpTransaction
from currency_exchanger.exchange_manager import ExchangeManager
from wallets.transactions_manager import TransactionsManager


class WalletOpsTest(unittest.TestCase):
    def setUp(self):
        self.exch_man = ExchangeManager()

    #def tearDown(self):
    #    # return Rates to default because test runs in production db:
    #    self.exch_man.set_rate(quote_currency="CAD", rate=1.26)

    def test_create_wallet(self):
        # test create wallet
        albert_wallet = Wallet.register_wallet(user_name="Albert", country="RU", city="Moscow", wallet_currency="CAD")
        print(albert_wallet)

    def test_fillup_wallet(self):
        ## test fill up wallet with some amount
        self.exch_man.set_rate(quote_currency="CAD", rate=1.26)
        wallet = Wallet.register_wallet(user_name="Albert", country="RU", city="Moscow", wallet_currency="CAD")
        bal0 = wallet.balance

        balance_diff = Money(100, 'EUR')
        localized_balance_diff = convert_money(balance_diff, wallet.balance.currency)

        wallet, transaction = Wallet.fillup_wallet(target_wallet=wallet, value=balance_diff)

        bal1 = wallet.balance
        self.assertAlmostEqual((bal1-bal0).amount, localized_balance_diff.amount)
        # precision loss
        #self.assertEqual((bal1-bal0).amount, localized_balance_diff.amount)

    ## test update exchange rate
    def test_update_exchange_rate(self):
        self.exch_man.set_rate(quote_currency="CAD", rate=1.46)
        usds = Money(100, 'USD')
        converted = convert_money(usds, "CAD")
        #import ipdb; ipdb.set_trace()
        self.assertAlmostEqual(float(converted.amount), 146.0)

    ## test transfer from wallet to wallet with third currency
    def test_transfer_with_multiconvertation(self):
        wallet0 = Wallet.register_wallet(
            user_name="Albert",
            country="RU",
            city="Moscow",
            wallet_currency="CAD")
        wallet1 = Wallet.register_wallet(
            user_name="Chen Hui",
            country="CN",
            city="Hong Kong",
            wallet_currency="CNY")

        #ExchangeRatesManager.set_rate("USD/CAD", Decimal(1.26))
        #ExchangeRatesManager.set_rate("USD/CNY", Decimal(6.9))
        #ExchangeRatesManager.set_rate("USD/EUR", Decimal(0.89))

        bal00 = wallet0.balance
        bal10 = wallet1.balance

        transfert_value = Money(15, 'USD')
        transact = Wallet.transfer_value(
            target_wallet=wallet1,
            value=transfert_value,
            source_wallet=wallet0
        )

        bal01 = wallet0.balance
        bal11 = wallet1.balance

        print(bal00, bal01)
        print(bal10, bal11)
        # TODO write automatic checks

    def test_get_report(self):
        # make wallets
        wallet0 = Wallet.register_wallet(
            user_name="Albert",
            country="Russia",
            city="Moscow",
            wallet_currency="CAD")
        balance_diff = Money(100, 'EUR')

        wallet, transaction = Wallet.fillup_wallet(target_wallet=wallet0, value=balance_diff)
        # make transaction
        # load transactions log
        transactions = TransactionsManager.get_report(wallet0, start_dt=None, fin_dt=None)
        print(transactions)

if __name__ == "__main__":
    unittest.main()

#

#
## test get report
#def test_get_report():
#    # make wallets
#    # make transaction
#    # load transactions log
#    transactions = TransactionsManager.get_report(wallet, start_dt=None, fin_dt=None)
#    pass
#
## test get report as csv
#def test_get_report_csv():
#    transactions = TransactionsManager.get_report(wallet, start_dt=None, fin_dt=None)
#
#    df = pd.DataFrame(list(transactions.values('author', 'date', 'slug')))
#    pass