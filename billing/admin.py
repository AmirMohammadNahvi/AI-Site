from django.contrib import admin

from .models import PaymentTransaction, Plan, PurchaseOrder, QuotaWindow, UserSubscription


admin.site.register(Plan)
admin.site.register(UserSubscription)
admin.site.register(QuotaWindow)
admin.site.register(PurchaseOrder)
admin.site.register(PaymentTransaction)
