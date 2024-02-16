from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('profile/<int:user_pk>', views.UserProfileView.as_view(), name='user_detail'),
    path('changepassword', views.change_password, name='change_password'),
    path('<int:user_pk>', views.user_appointments_view, name='user_appointments'),
    path('<int:doctor_pk>/create-appoint/', views.create_appoint_doctor, name='create_appointment'),
    path('<int:doctor_pk>/write-review', views.write_review_view, name='write_review'),
    path('<int:doc_pk>/doctor-details', views.doctor_detail_view, name='doctor_details'),
    path('<int:appoint_pk>/cancel-appointment', views.cancel_appointment_view, name='cancel_appointment'),
    path('dashboard/<int:doctor_pk>', views.doctor_dashboard, name='doctor_dashboard'),
    path('<int:patient_pk>/patient-details', views.patient_detail_view, name='patient_detail'),
    path('profile-pic/', views.change_profile_pic, name='change_profile_pic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

