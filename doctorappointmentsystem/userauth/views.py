from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterDoctorUserForm, CustomAuthenticationForm
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.shortcuts import render, redirect


class LoginUserView(View):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'user_type': 'User'})

    def post(self, request):
        error = None
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None and user.user_type == 'C':
                login(request, user)
                return redirect('index')
            else:
                error = True
        return render(request, self.template_name, {'form': form, 'user_type': 'User', 'error': error})

class LoginDoctorView(View):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'user_type': 'Doctor'})
    
    def post(self, request):
        error = None
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.user_cache
            if user is not None and user.user_type == 'D':
                login(request, user)
                return redirect('doctor_dashboard', user.pk)
            else:
                error = True
                
        return render(request, self.template_name, {'form': form, 'user_type': 'Doctor', 'error': error})

class RegisterUserView(View):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    initial = {'user_type': 'User'}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class RegisterDoctorView(View):
    template_name = 'registration/register.html'
    form_class = RegisterDoctorUserForm
    initial = {'user_type': 'Doctor'}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form, 'user_type': 'Doctor'})

