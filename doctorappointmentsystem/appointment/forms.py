from .models import Appointment, DoctorReview, User
from django import forms


class DoctorReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorReview
        fields = ['review']

class AppointmentCreateFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'end_time', 'date']

class ProfilePic(forms.ModelForm):
    class Meta:
        model = User
        fields = ['prifile_pic']