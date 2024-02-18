"""
URL configuration for doctorappointmentsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userauth import views as ua_views

from django.conf.urls.static import static
from django.conf import settings
from appointment.admin import admin_site

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin_site.urls),
    path('', include('appointment.urls')),
    path('login_user/', ua_views.LoginUserView.as_view(), name='login_user'),
    path('login_doctor/', ua_views.LoginDoctorView.as_view(), name='login_doctor'),
    path('user/register', ua_views.RegisterUserView.as_view(), name='register_user'),
    path('doctor/register', ua_views.RegisterDoctorView.as_view(), name='register_doctor'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
