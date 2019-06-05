from djmoney.models.fields import MoneyField
from django.db import models
from djmoney.money import Money, Currency
from django_countries.fields import CountryField
from djmoney.contrib.exchange.models import convert_money
from django.utils.text import slugify


# Create your models here.
class UserProfile(models.Model):
    """Payment system's User"""
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = CountryField()


class Wallet(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # free balance
    balance = MoneyField(max_digits=14, decimal_places=2, default=Money(0, 'USD'),
                         default_currency='USD')

    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)

    def _secret_hash(self):
        #generates secret hash for wallet to alias it in secret link
        import hashlib
        user_code = "%s %s %s" % (self.owner.name, self.owner.city , self.owner.country)
        #import ipdb; ipdb.set_trace()
        user_hash = hashlib.sha224(user_code.encode('utf8')).hexdigest()
        return user_hash

    def _get_unique_slug(self):
        print("preslug")
        text = str(self.balance.currency) + str(self._secret_hash())
        print(text)
        slug = slugify(text)
        print(slug)
        unique_slug = slug
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    @classmethod
    def register_wallet(cls, user_name, country, city, wallet_currency):
        print("register_wallet")
        # register user:
        up, created = UserProfile.objects.get_or_create(name=user_name,
                                                        country=country,
                                                        city=city)
        #print("created")
        #print(created)
        wallet_candidates = Wallet.objects.filter(owner=up)
        if len(wallet_candidates) == 1:
            # check currencies match:
            wallet = wallet_candidates[0]
            wallet_currency = Currency(wallet_currency)
            if wallet.balance.currency == wallet_currency:
                return wallet
            else:
                #print(wallet_currency)
                #print(type(wallet_currency))
                #print(wallet.balance.currency)
                #print(type(wallet.balance.currency))
                raise Exception("User already have Wallet with currency: %s" % wallet.balance.currency)
        elif len(wallet_candidates) > 1:
            # according to Requirements Doc user has only one wallet!
            raise Exception("Only one wallet for User allowed!")
        else:
            wallet = Wallet.objects.create(owner=up, balance=Money(0.0, wallet_currency))
            return wallet

    @classmethod
    def fillup_wallet(cls, target_wallet, value, source_broker=None):
        """
        Method implements Fill Up operation for Wallet
        """

        if not source_broker:
            source_broker, _ = FillUpBroker.objects.get_or_create()
        fillup_transaction = FillUpTransaction.objects.create(
            source_broker=source_broker,
            target_wallet=target_wallet,
            transfer_value=value
        )

        ###################################################################
        if value.currency != target_wallet.balance.currency:
            print("currencies mismatch!")
            converted_value = convert_money(value, target_wallet.balance.currency)
        else:
            converted_value = value
            ###################################################################

        # do we need to log initial currency amount?
        target_wallet.balance += converted_value
        target_wallet.save()
        return target_wallet, fillup_transaction

    @classmethod
    def transfer_value(cls, target_wallet, value, source_wallet):
        """
        Method implements transfer of value between Wallets
        """
        print("transfer_value")
        ###################################################################
        if value.currency != source_wallet.balance.currency:
            preconversion_value = convert_money(value, source_wallet.balance.currency)
        else:
            preconversion_value = value
            ###################################################################

        if preconversion_value > source_wallet.balance:
            print("Warning: attempt to send more value than own!")
            # no explicit prohibition for this in System Requirements Document

        source_wallet.balance -= preconversion_value

        ###################################################################
        if preconversion_value.currency != target_wallet.balance.currency:
            postconversion_value = convert_money(preconversion_value, target_wallet.balance.currency)
        else:
            postconversion_value = value
            ###################################################################

        target_wallet.balance += postconversion_value

        tr_transaction = TransferTransaction.objects.create(
            source_wallet=source_wallet,
            target_wallet=target_wallet,
            transfer_value=value
        )
        # now save update balances:
        source_wallet.save()
        target_wallet.save()
        return tr_transaction

    @classmethod
    def get_transactions_report(cls, target_wallet, start_dt, fin_dt):
        print("get_transactions_report")


class FillUpBroker(models.Model):
    """
    Broker for Filling Up operation
    """
    name = models.CharField(max_length=200, default="Default Fill Up Broker")

# ######## Financial Transactions #######################################
class AbstractFinancialTransaction(models.Model):
    class Meta:
        abstract = True

    transaction_type = models.CharField(max_length=200, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    target_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    # how much Money transferred
    transfer_value = MoneyField(max_digits=14, decimal_places=2, default=Money(0, 'USD'),
                                default_currency='USD')


class FillUpTransaction(AbstractFinancialTransaction):
    FILL_UP_TR_TYPE = "FillUp"

    # overload parent field
    transaction_type = models.CharField(max_length=20, null=False, default=FILL_UP_TR_TYPE)

    source_broker = models.ForeignKey(FillUpBroker, on_delete=models.CASCADE)


class TransferTransaction(AbstractFinancialTransaction):
    TRANSFER_TR_TYPE = "Transfer"
    # overload parent field
    transaction_type = models.CharField(max_length=20, null=False, default=TRANSFER_TR_TYPE)

    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transfers_by_source")