import os
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound
from django.http import FileResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings
from wallets.forms import RegistrationForm, FillUpWalletForm, SendMoneyForm, FilterTransactionsForm
from wallets.models import Wallet
from wallets.transactions_manager import TransactionsManager


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        registration_form = RegistrationForm(request.POST)
        # check whether it's valid:
        if registration_form.is_valid():
            # process the data in form.cleaned_data as required
            #Wallet.register_wallet(user_name, country, city, wallet_currency)
            wallet = Wallet.register_wallet(**registration_form.cleaned_data)
            # redirect to a wallet cabinet:
            return HttpResponseRedirect('/wallets/'+wallet.slug)

    # if a GET (or any other method) we'll create a blank form
    else:
        registration_form = RegistrationForm()

    wallets = Wallet.objects.all()
    template_path = 'wallets/index.html'
    context = {
        'wallets_list': wallets,
        'registration_form': registration_form
    }
    return render(request, template_path, context)


def view_wallet_cabinet(request, wallet_hash, *args, **kwargs):
    # load wallet obj
    try:
        wallet = Wallet.objects.get(slug=wallet_hash)
    except Exception as e:
        print(e)
        raise Http404("Wallet %s does not exist" % wallet_hash)

    fillup_wallet_form = FillUpWalletForm()
    send_money_form = SendMoneyForm()
    filter_transactions_form = FilterTransactionsForm()

    template = loader.get_template('wallets/wallet_cabinet.html')
    context = {
        'wallet': wallet,
        'fillup_wallet_form': fillup_wallet_form,
        'send_money_form': send_money_form,
        'filter_transactions_form': filter_transactions_form
    }
    return HttpResponse(template.render(context, request))


def fill_up_wallet(request, *args, **kwargs):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        fill_up_form = FillUpWalletForm(request.POST)
        # check whether it's valid:
        if fill_up_form.is_valid():
            money = fill_up_form.cleaned_data['money']
            target_wallet_id = fill_up_form.cleaned_data['wallet_id']
            try:
                wallet = Wallet.objects.get(id=target_wallet_id)
            except Exception as e:
                print(e)
                raise Http404("Wallet %s does not exist" % target_wallet_id)
            wallet, transaction = Wallet.fillup_wallet(wallet, money)
            return HttpResponse(
                "You've filled up the wallet %s with %s %s" % (money.amount, money.currency, target_wallet_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        fill_up_form = FillUpWalletForm(request.POST)

    template_path = 'wallets/fill_up_form.html'
    context = {
        'fill_up_form': fill_up_form
    }
    return render(request, template_path, context)


def send_money(request, wallet_hash):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        send_money_form = SendMoneyForm(request.POST)
        # check whether it's valid:
        if send_money_form.is_valid():
            money = send_money_form.cleaned_data['money']
            target_wallet_id = send_money_form.cleaned_data['target_wallet_id']
            try:
                target_wallet = Wallet.objects.get(id=target_wallet_id)
            except Exception as e:
                print(e)
                return Http404("Target wallet %s does not exist" % target_wallet_id)

            try:
                source_wallet = Wallet.objects.get(slug=wallet_hash)
            except Exception as e:
                print(e)
                raise Http404("Source wallet %s does not exist" % source_wallet)

            transaction = Wallet.transfer_value(target_wallet, money, source_wallet)
            return HttpResponse(
                "You've transfered %s to the wallet %s" % (money, target_wallet_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        send_money_form = SendMoneyForm()

    template_path = 'wallets/send_money_form.html'
    context = {
        'send_money_form': send_money_form
    }
    return render(request, template_path, context)


def filter_transactions(request, wallet_hash, *args, **kwargs):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        filter_transactions_form = FilterTransactionsForm(request.POST)
        # check whether it's valid:
        if filter_transactions_form.is_valid():
            params = {}
            wallet_id = filter_transactions_form.cleaned_data['wallet_id']
            try:
                target_wallet = Wallet.objects.get(id=wallet_id)
                params['wallet'] = target_wallet
            except Exception as e:
                print(e)
                return Http404("Target wallet %s does not exist" % wallet_id)

            # TODO:
            # parse dates
            params['start_dt'] = filter_transactions_form.cleaned_data['start_date']
            params['fin_dt'] = filter_transactions_form.cleaned_data['fin_date']
            #print(start_dt_raw)
            #print(fin_dt_raw)

            # check autorization of requester for checking transaction of target wallet?
            transactions_df = TransactionsManager.get_report(**params)
            print(transactions_df)
            # output format handling:
            as_csv = filter_transactions_form.cleaned_data['as_csv']
            if as_csv:
                # request for loading as CSV:
                filename = "transactions_%s.csv" % target_wallet.id
                file_location = os.path.join(settings.MEDIA_ROOT, filename)

                transactions_df.to_csv(file_location)

                try:
                    response = FileResponse(open(file_location, 'rb'), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename

                except IOError:
                    # handle file not exist case here
                    response = HttpResponseNotFound('<h1>File not exist</h1>')

                return response
            else:
                # request for inline representation:
                return HttpResponse(transactions_df.to_html())

    # if a GET (or any other method) we'll create a blank form
    else:
        filter_transactions_form = FilterTransactionsForm()

    template_path = 'wallets/filter_transactions_form.html'
    context = {
        'filter_transactions_form': filter_transactions_form
    }
    return render(request, template_path, context)