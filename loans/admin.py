from django.contrib import admin
from .models import LoanRecord

@admin.register(LoanRecord)
class LoanRecordAdmin(admin.ModelAdmin):
    list_display = ['sr', 'date', 'name', 'loan_amount', 'interest_rate', 'final_amount', 'status', 'balance']
    list_filter = ['status', 'interest_rate']
    search_fields = ['name']
    ordering = ['sr']
