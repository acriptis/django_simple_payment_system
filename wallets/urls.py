# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'wallets'
urlpatterns = [
    # ex: /wallets/
    path('', views.index, name='index'),

    path('fill_up_wallet', views.fill_up_wallet, name='fill_up_wallet'),
    path('<slug:wallet_hash>/send_money', views.send_money, name='send_money'),
    path('<slug:wallet_hash>/filter_transactions', views.filter_transactions, name='filter_transactions'),
    # ex: /wallets/sdf435sfwetw4t3wh/
    path('<slug:wallet_hash>/', views.view_wallet_cabinet, name='wallet_cabinet'),

]