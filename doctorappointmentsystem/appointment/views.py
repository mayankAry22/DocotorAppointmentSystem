from operator import concat
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import DoctorReviewForm, AppointmentCreateFormDoctor, ProfilePic
from .models import Appointment, Doctor, Customer, User
from .filters import DoctorFilter, AppointmentFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IndexPageView(LoginRequiredMixin, TemplateView):
    login_url = 'login_user'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin:index')

        doctors_list = Doctor.objects.filter(is_approved=True).order_by('id')
        myFilter = DoctorFilter(request.GET, queryset=doctors_list)
        doctors_list = myFilter.qs

        paginator = Paginator(doctors_list, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj,
            'myFilter': myFilter
        }
        return render(request, 'appointment/index.html', context)
    


class DoctorDetailView(View):

    def get(self, request, doc_pk):
        doctor_details = Doctor.objects.prefetch_related('doctorreview_set').filter(id=doc_pk)
        context = {
            'doctor_details': doctor_details
        }
        return render(request, 'appointment/doctor_detail.html', context)


def doc_profile_view(request, doc_pk):
    doctor_details = Doctor.objects.get(id = doc_pk)
    context = {
        'doctor_details': doctor_details
    }
    
    return render(request, 'appointment/doctor_detail.html', context)
    


def write_review_view(request, doctor_pk):
    if request.method == 'POST':
        form = DoctorReviewForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            doctor = Doctor.objects.get(id=doctor_pk)
            form.doctor_id = doctor
            form.save()
            return redirect('index')
        
    else:  
        form = DoctorReviewForm()
                
    return render(request, 'appointment/write_review.html', {'form': form})
    

def user_appointments_view(request, user_pk):
    appointment_details = Appointment.objects.select_related('doctor').filter(customer_id=user_pk).all()

    p = Paginator(appointment_details, 5)
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
        
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'appointment/user_appointments.html', context)


def cancel_appointment_view(request, appoint_pk):
    Appointment.objects.filter(id=appoint_pk).update(is_cancelled=True)
    
    if request.user.user_type == 'C':
        return redirect('user_appointments', user_pk = request.user.pk)
    else:
        return redirect('doctor_dashboard', doctor_pk = request.user.pk)

class UserProfileView(LoginRequiredMixin, DetailView):
    login_url = 'login_user'
    template_name = 'appointment/user_detail.html'
    model = None  # Set the model based on user_type
    form_class = ProfilePic

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.kwargs['user_pk']:
            return redirect('index')
        if request.user.user_type == 'C':
            self.model = Customer
        elif request.user.user_type == 'D':
            self.model = Doctor
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['user_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_details'] = context['object']
        context['form'] = self.form_class()
        return context


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'appointment/change_password.html', {'form': form })


def appoint_detail(request, doctor_pk, appoint_pk):
    appointment = get_object_or_404(Appointment, pk=appoint_pk)

    appoint_detail_data = {
        'title': appointment.start_time,
        'appointment': appointment,
    }

    return render(request, 'appointment/appoint_detail.html', appoint_detail_data)


def doctor_dashboard(request, doctor_pk):
    if request.user.is_authenticated and request.user.pk == doctor_pk and request.user.is_doctor():
        appointment_details = Appointment.objects.select_related('customer').filter(doctor_id=doctor_pk).all()
        
        myFilter = AppointmentFilter(request.GET, queryset=appointment_details)
        appointment_details = myFilter.qs
    
        p = Paginator(appointment_details, 5)
        page_number = request.GET.get('page')
        
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
            
        context = {
            'page_obj': page_obj,
            'myFilter': myFilter
        }
        
        return render(request, 'appointment/doctor_dashboard.html', context)
    else:
        raise Http404("ERROR: user is not authenticated.")
 

def patient_detail_view(request, patient_pk):
     cust_details = Customer.objects.get(id=patient_pk)
     print(patient_pk)
     print(cust_details)
     
     return render(request, 'appointment/customer_detail.html', { 'cust_details': cust_details })
 

def create_appoint_doctor(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)
    customer = get_object_or_404(Customer, pk=request.user.pk)

    if request.method == 'POST' and request.user is not None and doctor is not None:
        form = AppointmentCreateFormDoctor(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer
            appointment.doctor = doctor
            appointment.save()

            return redirect('index')
        else:
            raise Http404('Form is not valid')
    else:
        form = AppointmentCreateFormDoctor()

    return render(request, 'appointment/create_appoint.html', {'form': form, 'doctor': doctor, 'customer': customer})


def change_profile_pic(request):
    print(request.FILES.get('image'))
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        form = ProfilePic(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    
    return redirect('user_detail', user_pk=request.user.pk)
