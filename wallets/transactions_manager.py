# -*- coding: utf-8 -*-
from wallets.models import FillUpTransaction, TransferTransaction
import pandas as pd


class TransactionsManager():
    @classmethod
    def get_report(cls, wallet, start_dt=None, fin_dt=None):
        """
        make report as pandas DataFrame
        so it easy to manipulate
        """
        # collect FillUp transactions
        dt_params = {}
        if start_dt:
            dt_params['timestamp__gte'] = start_dt
        if fin_dt:
            dt_params['timestamp__lte'] = fin_dt
        fups = FillUpTransaction.objects.filter(target_wallet=wallet, **dt_params)
        list_of_dicts = [
            {'timestamp': each_tr.timestamp,
             'amount': each_tr.transfer_value.amount,
             'currency': each_tr.transfer_value.currency,
             'companion': each_tr.source_broker.name,
             'transaction_type': FillUpTransaction.FILL_UP_TR_TYPE
         } for each_tr in fups]

        trs_log_df = pd.DataFrame(list_of_dicts)

        # collect incoming transactions
        in_ttrs = TransferTransaction.objects.filter(target_wallet=wallet, **dt_params)
        list_of_dicts_in_ttrs = [
            {'timestamp': each_tr.timestamp,
             'amount': each_tr.transfer_value.amount,
             'currency': each_tr.transfer_value.currency,
             #'companion': each_tr.source_wallet.id,
             'companion': each_tr.source_wallet.owner.name,
             'transaction_type': TransferTransaction.TRANSFER_TR_TYPE
         } for each_tr in in_ttrs ]

        trs_log_df_in_ttrs = pd.DataFrame(list_of_dicts_in_ttrs)

        # collect outgoing transactions
        out_ttrs = TransferTransaction.objects.filter(source_wallet=wallet, **dt_params)
        list_of_dicts_out_ttrs = [
            {'timestamp': each_tr.timestamp,
             'amount': -each_tr.transfer_value.amount,
             'currency': each_tr.transfer_value.currency,
             'companion': each_tr.target_wallet.owner.name,
             'transaction_type': TransferTransaction.TRANSFER_TR_TYPE
         } for each_tr in out_ttrs]

        trs_log_df_out_ttrs = pd.DataFrame(list_of_dicts_out_ttrs)

        # merge DataFrames:
        merged_report = trs_log_df.append(other=[trs_log_df_in_ttrs, trs_log_df_out_ttrs])
        # sort by date:
        #import ipdb; ipdb.set_trace()
        if len(merged_report) > 0:
            merged_report.sort_values(by='timestamp', inplace=True)

            merged_report.set_index('timestamp', inplace=True)
        return merged_report
