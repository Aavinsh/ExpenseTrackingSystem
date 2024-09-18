from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if request.method=="POST":
        expense_form=ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense=expense_form.save(commit=False)
            expense.user_id=request.user.id
            expense.save()  
    
    # expenses =Expense.objects.all() 
    expenses=Expense.objects.filter(user=request.user)
    total_expenses=expenses.aggregate(Sum('amount'))

    #Logic to calculate 365 days expenses
    last_year=datetime.date.today() - datetime.timedelta(days=365)
    data= Expense.objects.filter(date__gt=last_year).filter(user=request.user)
    yearly_sum=data.aggregate(Sum('amount'))

     #Logic to calculate 30 days expenses
    last_month=datetime.date.today() - datetime.timedelta(days=30)
    data= Expense.objects.filter(date__gt=last_month).filter(user=request.user)
    monthly_sum=data.aggregate(Sum('amount'))
    
     #Logic to calculate 365 days expenses
    last_week=datetime.date.today() - datetime.timedelta(days=7)
    data= Expense.objects.filter(date__gt=last_week).filter(user=request.user)
    weekly_sum=data.aggregate(Sum('amount'))
    
    #Logic to calculate the expenses onthe basic of date
    daily_sum= Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount')).filter(user=request.user)
   
    #Logic to calculate expenses onthe basic of category
    categorical_sum= Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount')).filter(user=request.user)
    

    expense_form=ExpenseForm()
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum ,'daily_sum':daily_sum,'categorical_sum':categorical_sum})

def edit(request,id): 
    expense=Expense.objects.get(id=id)
    edit_form=ExpenseForm(instance=expense)
    if request.method=="POST":
        expense=Expense.objects.get(id=id)
        form=ExpenseForm(request.POST,instance=expense) 
        if form.is_valid:
            form.save()
            return redirect('index')
    return render(request,'myapp/edit.html',{'edit_form':edit_form} )

def delete(request,id):
    if request.method=='POST':
        expense=Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')