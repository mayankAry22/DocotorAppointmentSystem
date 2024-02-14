from django.contrib.auth.forms import UserCreationForm
from appointment.models import Customer, Doctor

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'phone_no', 'email', 
                  'gender', 'password1', 'password2']


class RegisterDoctorUserForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ['username', 'first_name', 'last_name', 'doc_email', 
                  'specialization', 'location', 'fee', 'experiences', 'password1', 'password2']
        
        
        