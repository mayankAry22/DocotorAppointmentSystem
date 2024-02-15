from .models import Appointment, DoctorReview
from django import forms


class DoctorReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorReview
        fields = ['review']

class AppointmentCreateFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'end_time', 'date']