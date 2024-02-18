from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from appointment.models import Customer, Doctor, User
from django import forms
from django.utils.translation import gettext_lazy as _

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'phone_no', 'email', 
                  'gender', 'password1', 'password2']


class RegisterDoctorUserForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ['username', 'first_name', 'last_name', 'phone_no', 'email', 
                  'specialization', 'location', 'fee', 'experience', 'password1', 'password2']
        
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_('Mobile/Email'), max_length=254)
    
    error_messages = {
        'invalid_login': "Please enter a correct email or mobile number and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = None
            if User.objects.filter(email=username).exists():
                user = User.objects.get(email=username)
            elif User.objects.filter(phone_no=username).exists():
                user = User.objects.get(phone_no=username)

            if user is None or not user.check_password(password):
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

            self.user_cache = (
                user
                if user.email == username or user.phone_no == username
                else None
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            if self.user_cache is not None and not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
                
        return self.cleaned_data