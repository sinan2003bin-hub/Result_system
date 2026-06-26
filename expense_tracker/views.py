from calendar import month
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect("expense_home")
        
        return render(request, "expense_tracker/login.html", 
                {
                    "error": "Password or username is incorrect"
                }
            )
    
    return render(request, 'expense_tracker/login.html')

def signup(request):

    if request.method == "POST":

        username = request.POST["username"]
 
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:

            return render(request,"expense_tracker/signup.html",
                {
                    "error":"Passwords do not match"
                }
            )

        if User.objects.filter(username=username).exists():

            return render(request,"expense_tracker/signup.html",
                {
                    "error": "Username already exists"
                }
            )

        User.objects.create_user(
            username=username,
            password=password,
        )

        return redirect("login")

    return render(request,"expense_tracker/signup.html")


@login_required
def add_expense(request):
    name = request.POST['name']
    amount = request.POST['amount']

    Expense.objects.create(
        user=request.user,
        name=name,
        amount=amount
    )


@login_required
def clear_expenses(request):
    Expense.objects.filter(user=request.user).delete()


@login_required
def get_monthly_total(request):

    now = timezone.now()

    total = Expense.objects.filter(
        user=request.user,
        created_at__month=now.month,
        created_at__year=now.year
    ).aggregate(total=Sum('amount'))['total']

    return total or 0

@login_required
def delete_expense(request, id):

    expense = get_object_or_404(Expense, id=id, user=request.user)

    expense.delete()

    return redirect('expense_home')

@login_required
def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        expense.name = request.POST['name']
        expense.amount = request.POST['amount']
        date = request.POST['date']

        date_obj = datetime.strptime(date,"%Y-%m-%d")

        old_time = expense.created_at.time()

        expense.created_at = timezone.make_aware(
            datetime.combine(date_obj, old_time))
    
        expense.save()
        return redirect('expense_home')

    return render(request, 'expense_tracker/edit.html', {
        'expense': expense
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):

    success = None
    
    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')

    search = request.GET.get('search')

    if search:
        expenses = expenses.filter(name__icontains=search)

    total = sum(e.amount for e in expenses)
    action = None
    
    selected_month_total = None
    month = request.GET.get('month')

    if month:

        year, month_number = month.split('-')

        selected_month_total = Expense.objects.filter(
        user=request.user,
        created_at__year=year,
        created_at__month=month_number
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    selected_item_total = None

    item_name = request.GET.get('item_total')

    if item_name:

        selected_item_total = Expense.objects.filter(
        user=request.user,
        name__icontains=item_name
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    if request.method == 'POST':

        action = request.POST['action']

        if action == 'add':
            add_expense(request)
            success = 'Expense added successfully 😼'

        
        elif action == 'clear':
            clear_expenses(request)
            return redirect('expense_home')
        
        elif action == 'show':

            expenses = Expense.objects.filter(user=request.user).order_by('-created_at')

        elif action == 'edit':
            pass

    return render(request, 'expense_tracker/home.html', {
        'expenses': expenses,
        'monthly_total': get_monthly_total(request),
        'total': total,
        'action': action,
        'selected_month_total': selected_month_total,
        'selected_item_total': selected_item_total,
        'success': success
    })
