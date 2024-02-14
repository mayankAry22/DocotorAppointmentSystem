from .models import Appointment, DoctorReview
from django import forms


class DoctorReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorReview
        fields = ['review']
