# -*- coding: utf-8 -*-
from django.contrib import admin

from djmoney.contrib.exchange.models import Rate, ExchangeBackend


class RateAdmin(admin.ModelAdmin):
    list_display = ("currency", "value", "last_update", "backend")
    list_filter = ("currency",)
    ordering = ("currency",)

    def last_update(self, instance):
        return instance.backend.last_update

# unregister admin from django-money:
admin.site.unregister(Rate)
# register own admin:
admin.site.register(Rate, RateAdmin)



class ExchangeBackendAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExchangeBackend, ExchangeBackendAdmin)
