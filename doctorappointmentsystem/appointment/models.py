from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
import datetime


class User(AbstractUser):
    type_choices = (
        ('D', 'Doctor'),
        ('C', 'Customer')
    )
    
    gender_type = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    user_type = models.CharField('Type', max_length=1, choices=type_choices, default='C')
    first_name = models.CharField('First name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)
    gender = models.CharField('Gender', max_length=1, choices=gender_type, default='M')
    prifile_pic = models.ImageField(upload_to='images/', null=True, blank=True)
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_no = models.CharField(validators=[mobile_regex], max_length=17, unique=True)
    email = models.EmailField(unique=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return '/%i' % self.pk

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def is_customer(self):
        """Return True if User is Customer, else False"""
        return self.user_type == 'C'

    def is_doctor(self):
        """Return True if User is Doctor, else False"""
        return self.user_type == 'D'
    
    @property
    def image_url(self):
        return getattr(self.prifile_pic, 'url', None) if self.prifile_pic else None


class DoctorManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='D')


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='C')


class Doctor(User):
    objects = DoctorManager()
    specialization = models.CharField('Specialization', max_length=50)
    location = models.CharField('Location', max_length=50)
    experience = models.CharField('Experience', max_length=50)
    fee = models.IntegerField('Fee')
    is_approved = models.BooleanField('Approve', default=False)

    class Meta:
        ordering = ['specialization', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = 'D'
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return '/%i' % self.pk

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class DoctorReview(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review = models.TextField('Review', max_length=200, blank=False)


class Customer(User):
    objects = CustomerManager()

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = 'C'
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/profile/{self.pk}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Appointment(models.Model):
    start_time = models.TimeField('Start time')
    end_time = models.TimeField('End time')
    date = models.DateField('Date')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField("Cancelled", default = False)
    is_approved = models.BooleanField("Approved", default = False)
    is_completed = models.BooleanField("Completed", default = False)

    class Meta:
        ordering = ['start_time', '-date']

    def __str__(self):
        return str(self.start_time)

    def get_absolute_url(self):
        return f'/{self.doctor.id}/appoint/{self.id}'

    def is_outdated(self):
        today = datetime.datetime.now()
        day = datetime.datetime.combine(self.date, self.start_time)
        return day <= today

    def is_working_day_appointment(self):
        return 0 <= self.date.weekday() <= 4

    is_outdated.boolean = True
    is_outdated.short_description = 'Is Outdated?'

    is_working_day_appointment.boolean = True
    is_working_day_appointment.short_description = 'Is in working day?'
