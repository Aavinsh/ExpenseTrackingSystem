from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successfull")
            return redirect('register')
        else:
            return render(request,'register.html',{'form':form})
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request,'register.html',context)

def login(request):
    if request.method=="POST":
         form= AuthenticationForm(request, request.POST)
         if form.is_valid():
             username=form.cleaned_data['username']
             password=form.cleaned_data['password']
             user=auth.authenticate(username=username,password=password)

             if user is not None:
                 auth.login(request,user)
                 return redirect('index')
         else:
             messages.error(request,'Incorrect Username or password')
             return redirect('login')          
    else:
        form=AuthenticationForm()
        context={
            'form':form,
        }
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('login')