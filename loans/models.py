from django.db import models
from django.contrib.auth.models import User


class LoanRecord(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('emergency', 'Emergency'),
    ]

    sr = models.PositiveIntegerField(unique=True, verbose_name="Sr No.")
    date = models.DateField(verbose_name="Date")
    name = models.CharField(max_length=100, verbose_name="Name")
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Loan Amount (₹)")
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Interest (₹)")
    interest_rate = models.CharField(max_length=10, default='0%', verbose_name="Interest Rate")
    duration = models.CharField(max_length=50, blank=True, null=True, verbose_name="Duration")
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Final Amount (₹)")
    paid_date = models.DateField(blank=True, null=True, verbose_name="Paid Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Balance Due (₹)")
    remark = models.CharField(max_length=200, blank=True, default='', verbose_name="Remark")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_loans')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sr']
        verbose_name = "Loan Record"
        verbose_name_plural = "Loan Records"

    def __str__(self):
        return f"#{self.sr} - {self.name} - ₹{self.loan_amount}"

    @property
    def received_amount(self):
        return self.loan_amount - self.balance
