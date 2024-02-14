import django_filters
from .models import Doctor

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'location']