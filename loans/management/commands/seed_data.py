from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from loans.models import LoanRecord
from datetime import date

class Command(BaseCommand):
    help = 'Seed initial loan data and create admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', '', 'admin123', is_staff=True)
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / admin123'))
        if not User.objects.filter(username='viewer').exists():
            User.objects.create_user('viewer', '', 'viewer123', is_staff=False)
            self.stdout.write(self.style.SUCCESS('Viewer user created: viewer / viewer123'))

        LoanRecord.objects.all().delete()
        loans = [
            dict(sr=1,  date=date(2024,4,9),  name='Pravin Rewale',  loan_amount=20000, interest=800,  interest_rate='1%', duration='5 Month',   final_amount=20800, paid_date=date(2024,9,24),  status='paid',      balance=0,     remark='Clear'),
            dict(sr=2,  date=date(2024,4,18), name='Akshay Rewale',  loan_amount=30000, interest=3600, interest_rate='2%', duration='7 month',   final_amount=33600, paid_date=date(2024,11,14), status='paid',      balance=0,     remark='Clear'),
            dict(sr=3,  date=date(2024,5,11), name='Dilip Sukam',    loan_amount=5000,  interest=500,  interest_rate='1%', duration='5 month',   final_amount=5500,  paid_date=date(2025,2,26),  status='paid',      balance=0,     remark='Clear'),
            dict(sr=4,  date=date(2024,7,1),  name='Pravin Rewale',  loan_amount=20000, interest=3450, interest_rate='2%', duration='18 month',  final_amount=23450, paid_date=date(2026,1,2),   status='paid',      balance=0,     remark='Clear'),
            dict(sr=5,  date=date(2024,8,2),  name='Yogesh Sukam',   loan_amount=10000, interest=1200, interest_rate='1%', duration='',          final_amount=0,     paid_date=None,             status='pending',   balance=2000,  remark='Partial paid'),
            dict(sr=6,  date=date(2024,8,12), name='Rupesh Gavade',  loan_amount=10000, interest=200,  interest_rate='1%', duration='2 Month',   final_amount=10200, paid_date=date(2024,10,12), status='paid',      balance=0,     remark='Clear'),
            dict(sr=7,  date=date(2024,9,1),  name='Nitesh Sukam',   loan_amount=12000, interest=240,  interest_rate='1%', duration='2 Month',   final_amount=12240, paid_date=date(2024,10,14), status='paid',      balance=0,     remark='Clear'),
            dict(sr=8,  date=date(2024,9,24), name='Rupesh Sukam',   loan_amount=10000, interest=0,    interest_rate='0%', duration='Emergency', final_amount=10000, paid_date=date(2025,1,29),  status='emergency', balance=0,     remark='Clear'),
            dict(sr=9,  date=date(2024,12,1), name='Vaibhav Sukam',  loan_amount=30000, interest=8800, interest_rate='2%', duration='',          final_amount=0,     paid_date=None,             status='pending',   balance=10000, remark='Partial paid'),
            dict(sr=10, date=date(2025,3,8),  name='Rupesh Gavade',  loan_amount=10000, interest=2800, interest_rate='2%', duration='13 month',  final_amount=12800, paid_date=date(2026,4,27),  status='paid',      balance=0,     remark='Clear'),
            dict(sr=11, date=date(2025,9,17), name='Dilip Sukam',    loan_amount=10000, interest=600,  interest_rate='2%', duration='',          final_amount=0,     paid_date=None,             status='pending',   balance=1000,  remark='Partial paid'),
            dict(sr=12, date=date(2025,10,13),name='Rupesh Sukam',   loan_amount=0,     interest=200,  interest_rate='2%', duration='Emergency', final_amount=200,   paid_date=None,             status='emergency', balance=0,     remark='Clear'),
            dict(sr=13, date=date(2025,10,11),name='Nitesh Sukam',   loan_amount=20000, interest=400,  interest_rate='2%', duration='1 month',   final_amount=20400, paid_date=date(2025,10,23), status='paid',      balance=0,     remark='Clear'),
            dict(sr=14, date=date(2025,12,9), name='Roshan Rewale',  loan_amount=30000, interest=1200, interest_rate='2%', duration='2 Month',   final_amount=31200, paid_date=date(2026,2,24),  status='paid',      balance=0,     remark='Clear'),
            dict(sr=15, date=date(2026,4,12), name='Rupesh Sukam',   loan_amount=20000, interest=0,    interest_rate='2%', duration='',          final_amount=20000, paid_date=None,             status='pending',   balance=20000, remark=''),
            dict(sr=16, date=date(2026,4,13), name='Pravin Rewale',  loan_amount=10000, interest=400,  interest_rate='2%', duration='',          final_amount=10000, paid_date=None,             status='pending',   balance=8000,  remark='Partial paid'),
        ]
        for l in loans:
            LoanRecord.objects.create(**l)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(loans)} loan records.'))
