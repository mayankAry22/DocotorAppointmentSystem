from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterDoctorUserForm
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def login_user(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.user_type == 'C':
               form = login(request, user)
               return redirect('index')
            else:
               error = True
        else:
            error = True
       
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form, 'user_type': 'User', 'error': error})

def login_doctor(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.user_type == 'D':
               form = login(request, user)
               return redirect('doctor_dashboard', user.pk)
            else:
               error = True
        else:
            error = True
       
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form , 'user_type': 'Doctor', 'error': error})

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register.html', {'form': form, 'user_type': 'User'})



def register_doctor(request):
    if request.method == 'POST':
        form = RegisterDoctorUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            raise Http404('Form is not valid')
    else:
        form = RegisterDoctorUserForm()

    return render(request, 'registration/register.html', {'form': form, 'user_type': 'Doctor'})

