from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        exclude = ['user', 'created_at', 'updated_at']  # Exclude user, created_at, and updated_at fields