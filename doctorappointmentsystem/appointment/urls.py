from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
   # path('<int:pk>', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('profile/<int:user_pk>', views.user_profile, name='user_detail'),
    path('changepassword', views.change_password, name='change_password'),
    path('<int:user_pk>/appointments', views.user_appointments_view, name='user_appointments'),
    path('<int:doctor_pk>/appoint', views.create_appoint_doctor, name='create_appointment'),
    path('<int:doctor_pk>/review', views.write_review_view, name='write_review'),
    path('<int:doc_pk>/doctor-details', views.doctor_detail_view, name='doctor_details'),
    path('<int:appoint_pk>', views.cancel_appointment_view, name='cancel_appointment'),
    path('dashboard/<int:doctor_pk>', views.doctor_dashboard, name='doctor_dashboard'),
]