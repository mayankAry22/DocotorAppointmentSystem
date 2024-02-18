from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('profile/<int:user_pk>', views.UserProfileView.as_view(), name='user_detail'),
    path('changepassword', views.ChangePasswordView.as_view(), name='change_password'),
    path('<int:user_pk>', views.UserAppointmentsView.as_view(), name='user_appointments'),
    path('<int:doctor_pk>/create-appoint/', views.CreateAppointmentDoctorView.as_view(), name='create_appointment'),
    path('<int:doctor_pk>/write-review', views.WriteReviewView.as_view(), name='write_review'),
    path('<int:doc_pk>/doctor-details', views.DoctorDetailView.as_view(), name='doctor_details'),
    path('<int:pk>/approve-appointment', views.ApproveAppointmentView.as_view(), name='approve_appointment'),
    path('<int:pk>/complete-appointment', views.CompleteAppointmentView.as_view(), name='complete_appointment'),
    path('<int:pk>/cancel-appointment', views.CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('dashboard/<int:doctor_pk>', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('<int:patient_pk>/patient-details', views.PatientDetailView.as_view(), name='patient_detail'),
    path('profile-pic/', views.changeProfilePic.as_view(), name='change_profile_pic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

