from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        exclude = ['user', 'created_at', 'updated_at']  # Exclude user, created_at, and updated_at fields


from django import forms
from .models import FundsTransaction

class FundsTransactionForm(forms.ModelForm):
    class Meta:
        model = FundsTransaction
        exclude = ['payment_method', 'created_at', 'updated_at']  # Exclude these fields


from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['user', 'created_at', 'updated_at', 'payment_method']
    