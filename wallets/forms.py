# -*- coding: utf-8 -*-
from django import forms
from djmoney.forms import MoneyField
from django_countries.fields import CountryField
from django.conf import settings


class MoneyForm(forms.Form):
    money = MoneyField(
        currency_choices=[("SEK", "Swedish Krona")], max_value=1000, min_value=2)


class RegistrationForm(forms.Form):
    user_name = forms.CharField(label='Your name', max_length=100)
    city = forms.CharField(label='Your city', max_length=100)
    country = CountryField().formfield()
    #currency = forms.CharField(label='Desired currency', max_length=100)
    #currency = forms.Select(choices=settings.CURRENCY_CHOICES)
    wallet_currency = forms.ChoiceField(choices=settings.CURRENCY_CHOICES, label="Desired currency")


class FillUpWalletForm(forms.Form):
    money = MoneyField(label="Amount of money")
    wallet_id = forms.CharField(label='Wallet id to fill up', max_length=100, required=False, help_text="Enter it if you fill up someone other's wallet")


class SendMoneyForm(forms.Form):
    """
    Form for sending from Wallet cabinet
    """
    target_wallet_id = forms.CharField(label='Recepient wallet address', max_length=100)
    money = MoneyField(label="Amount of money to send")


#from django.contrib.admin import widgets

class FilterTransactionsForm(forms.Form):
    wallet_id = forms.CharField(label='Wallet id', max_length=100)
    start_date = forms.DateTimeField(label="Date from", required=False)
    fin_date = forms.DateTimeField(label="Date until", required=False)
    #fin_date2 = forms.SplitDateTimeField(label="Date until2", required=False)
    as_csv = forms.BooleanField(label="Load as CSV file", required=False)

    #def __init__(self, *args, **kwargs):
    #    super(FilterTransactionsForm, self).__init__(*args, **kwargs)
    #    #self.fields['mydate'].widget = widgets.AdminDateWidget()
    #    #self.fields['mytime'].widget = widgets.AdminTimeWidget()
    #    self.fields['fin_date2'].widget = widgets.AdminSplitDateTime()
    ##currency = forms.CharField(label='Desired currency', max_length=100)
