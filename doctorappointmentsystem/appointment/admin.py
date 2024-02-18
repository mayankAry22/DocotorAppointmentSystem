from django.contrib import admin
from .models import Appointment, Doctor, Customer, User

# Register other models as needed

class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['user_count'] = Doctor.objects.count() + Customer.objects.count()
        return super().index(request, extra_context=extra_context)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'phone_no')

    list_filter = ['first_name', 'last_name', 'gender', 'phone_no']

    search_fields = ['first_name', 'last_name', 'gender', 'phone_no']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'date', 'doctor', 'is_outdated',
                    'is_working_day_appointment')

    list_filter = ['start_time', 'end_time', 'date', 'doctor']

    search_fields = ['start_time', 'end_time', 'date', 'doctor']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'location', 'fee', 'is_approved')
    list_filter = ['first_name', 'last_name', 'specialization', 'location', 'fee', 'is_approved']
    search_fields = ['first_name', 'last_name', 'specialization', 'location', 'fee', 'is_approved']


admin_site = CustomAdminSite(name='customadmin')
admin_site.register(Doctor, DoctorAdmin)
admin_site.register(Customer, CustomerAdmin)
admin_site.register(Appointment, AppointmentAdmin)




