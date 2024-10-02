from django.contrib import admin

# Register your models here.

from .models import PaymentMethod, FundsTransaction

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'method_name', 'method_type', 'additional_details')
    # search_fields = ('user__username', 'method_name')
    # list_filter = ('method_type',)

@admin.register(FundsTransaction)
class FundsTransactionAdmin(admin.ModelAdmin):
    list_display = ('payment_method', 'amount', 'source_details')
    # search_fields = ('payment_method__method_name', 'source_details')
    # list_filter = ('payment_method__method_type',)


from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'category', 'payment_method', 'description')
    # search_fields = ('user__username', 'category', 'description')
    # list_filter = ('category', 'payment_method')