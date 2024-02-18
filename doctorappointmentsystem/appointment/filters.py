import django_filters
from .models import Doctor, Appointment

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'location']
        
class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['start_time', 'end_time', 'date', 'is_approved', 'is_completed', 'is_cancelled']