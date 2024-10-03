from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('bank_account', 'Bank Account'),
        ('credit_card', 'Credit Card'),
        ('digital_wallet', 'Digital Wallet'),
        ('other','Other'),
        
        # Add more payment types here if needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods', verbose_name="User")
    method_name = models.CharField(max_length=255, verbose_name="Payment Method Name")
    method_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, verbose_name="Payment Type")
    additional_details = models.TextField(blank=True, null=True, verbose_name="Additional Details")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        unique_together = ('user', 'method_name')
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return f"{self.user.username} - {self.method_name}"


class FundsTransaction(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='funds_transactions', verbose_name="Payment Method")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    source_details = models.TextField(blank=True, null=True, verbose_name="Source Details")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.amount} - {self.payment_method.method_name} ({self.source_details})"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses', verbose_name="User")
    date = models.DateField(default=timezone.now, verbose_name="Date")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category")
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, related_name='expenses', verbose_name="Payment Method")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"

    class Meta:
        verbose_name_plural = "Expenses"
        ordering = ['-date']  # Orders expenses by date in descending order
