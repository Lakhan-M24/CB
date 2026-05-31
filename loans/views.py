from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from decimal import Decimal
from .models import LoanRecord
from .forms import LoanRecordForm


# ─── Auth Views ───────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'loans/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    loans = LoanRecord.objects.all()

    # Search & filter (admin + viewer)
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    if search:
        loans = loans.filter(name__icontains=search)
    if status_filter:
        loans = loans.filter(status=status_filter)

    # If regular user, only show their own name's records
    if not request.user.is_staff:
        loans = LoanRecord.objects.filter(name__icontains=request.user.get_full_name() or request.user.username)

    agg = LoanRecord.objects.aggregate(
        total_loan=Sum('loan_amount'),
        total_interest=Sum('interest'),
        total_balance=Sum('balance'),
        total_final=Sum('final_amount'),
    )
    paid_count = LoanRecord.objects.filter(status='paid').count()
    pending_count = LoanRecord.objects.filter(status='pending').count()
    total_count = LoanRecord.objects.count()
    recovery = round((paid_count / total_count * 100) if total_count else 0)

    context = {
        'loans': loans,
        'search': search,
        'status_filter': status_filter,
        'total_loan': agg['total_loan'] or 0,
        'total_interest': agg['total_interest'] or 0,
        'total_balance': agg['total_balance'] or 0,
        'total_final': agg['total_final'] or 0,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'recovery': recovery,
    }
    return render(request, 'loans/dashboard.html', context)


# ─── Admin-only CRUD ──────────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def add_loan(request):
    if request.method == 'POST':
        form = LoanRecordForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.created_by = request.user
            loan.save()
            messages.success(request, f'Loan #{loan.sr} for {loan.name} added successfully.')
            return redirect('dashboard')
    else:
        # Auto-set next Sr number
        last = LoanRecord.objects.order_by('-sr').first()
        initial_sr = (last.sr + 1) if last else 1
        form = LoanRecordForm(initial={'sr': initial_sr})
    return render(request, 'loans/loan_form.html', {'form': form, 'action': 'Add'})


@admin_required
def edit_loan(request, pk):
    loan = get_object_or_404(LoanRecord, pk=pk)
    if request.method == 'POST':
        form = LoanRecordForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, f'Loan #{loan.sr} updated successfully.')
            return redirect('dashboard')
    else:
        form = LoanRecordForm(instance=loan)
    return render(request, 'loans/loan_form.html', {'form': form, 'action': 'Edit', 'loan': loan})


@admin_required
def delete_loan(request, pk):
    loan = get_object_or_404(LoanRecord, pk=pk)
    if request.method == 'POST':
        sr = loan.sr
        name = loan.name
        loan.delete()
        messages.success(request, f'Loan #{sr} for {name} deleted.')
        return redirect('dashboard')
    return render(request, 'loans/confirm_delete.html', {'loan': loan})


# ─── User Management (admin only) ─────────────────────────────────────────────

@admin_required
def manage_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'loans/manage_users.html', {'users': users})


@admin_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        is_staff = request.POST.get('is_staff') == 'on'
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                u = User.objects.create_user(username=username, password=password,
                                             first_name=first_name, last_name=last_name,
                                             is_staff=is_staff)
                messages.success(request, f'User "{username}" created.')
                return redirect('manage_users')
        else:
            messages.error(request, 'Username and password are required.')
    return render(request, 'loans/add_user.html')


@admin_required
def delete_user(request, uid):
    user = get_object_or_404(User, pk=uid)
    if user == request.user:
        messages.error(request, "You can't delete your own account.")
        return redirect('manage_users')
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User deleted.')
        return redirect('manage_users')
    return render(request, 'loans/confirm_delete_user.html', {'target_user': user})


# ─── Pending Summary ──────────────────────────────────────────────────────────

@login_required
def pending_summary(request):
    pending = LoanRecord.objects.filter(status='pending').order_by('sr')
    total_pending = pending.aggregate(total=Sum('balance'))['total'] or 0
    return render(request, 'loans/pending.html', {'pending': pending, 'total_pending': total_pending})
