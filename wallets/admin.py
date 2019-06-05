from django.contrib import admin
from wallets.models import Wallet, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    #list_display = ("owner", "balance", "slug")
    pass

admin.site.register(UserProfile, UserProfileAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = ("owner", "balance", "slug")
    pass

admin.site.register(Wallet, WalletAdmin)