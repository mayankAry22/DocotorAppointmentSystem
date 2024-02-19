from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import DoctorReviewForm, AppointmentCreateForm, ProfilePic
from .models import Appointment, Doctor, Customer, User
from .filters import DoctorFilter, AppointmentFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import (
    DetailView, TemplateView, UpdateView, FormView, ListView, CreateView, RedirectView
)


class IndexPageView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin:index')
        elif request.user.user_type == 'D':
            return redirect('doctor_dashboard', request.user.pk)

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

 

class WriteReviewView(View):
    def get(self, request, doctor_pk):
        form = DoctorReviewForm(initial={'doctor_id': doctor_pk})
        return render(request, 'appointment/write_review.html', {'form': form})

    def post(self, request, doctor_pk):
        form = DoctorReviewForm(request.POST)
        if not form.is_valid():
            return render(request, 'appointment/write_review.html', {'form': form})
        review = form.save(commit=False)
        doctor = Doctor.objects.get(id=doctor_pk)
        review.doctor_id = doctor
        review.save()
        return redirect('index')
    

class UserAppointmentsView(ListView):
    model = Appointment
    template_name = 'appointment/user_appointments.html'
    context_object_name = 'appointment_details'
    paginate_by = 5

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        return Appointment.objects.select_related('doctor').filter(customer_id=user_pk).all()
    

class ApproveAppointmentView(View):
    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs['pk'])
        appointment.is_approved = True
        appointment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

class CompleteAppointmentView(View):
    def get(self,request,  *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs['pk'])
        appointment.is_completed = True
        appointment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CancelAppointmentView(RedirectView):

    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs['pk'])
        appointment.is_cancelled = True
        appointment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserProfileView(DetailView):
    template_name = 'appointment/user_detail.html'
    model = None 
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


class ChangePasswordView(FormView):
    template_name = 'appointment/change_password.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DoctorDashboardView(ListView):
    model = Appointment
    template_name = 'appointment/doctor_dashboard.html'
    context_object_name = 'appointment_list'
    paginate_by = 5

    def get_queryset(self):
        doctor_pk = self.kwargs['doctor_pk']
        if self.request.user.is_authenticated and self.request.user.pk == doctor_pk and self.request.user.is_doctor():
            appointment_details = Appointment.objects.select_related('customer').filter(doctor_id=doctor_pk)
            return appointment_details
        else:
            raise Http404("ERROR: user is not authenticated.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        myFilter = AppointmentFilter(self.request.GET, queryset=self.get_queryset())
        appointment_details = myFilter.qs
        
        p = Paginator(appointment_details, self.paginate_by)
        page_number = self.request.GET.get('page')
        
        try:
            page_obj = p.page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        context['page_obj'] = page_obj
        context['myFilter'] = myFilter
        return context
 

class PatientDetailView(DetailView):
    model = Customer
    template_name = 'appointment/customer_detail.html'
    context_object_name = 'cust_details'

    def get_object(self, queryset=None):
        return Customer.objects.get(id=self.kwargs['patient_pk'])
 

class CreateAppointmentDoctorView(CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    template_name = 'appointment/create_appoint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor, pk=self.kwargs['doctor_pk'])
        context['customer'] = get_object_or_404(Customer, pk=self.request.user.pk)
        return context

    def form_valid(self, form):
        doctor = get_object_or_404(Doctor, pk=self.kwargs['doctor_pk'])
        customer = get_object_or_404(Customer, pk=self.request.user.pk)
        form.instance.doctor = doctor
        form.instance.customer = customer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class changeProfilePic(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        form = ProfilePic(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
        return redirect('user_detail', user_pk=request.user.pk)
