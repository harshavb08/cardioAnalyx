from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('patient_analyst/', views.analyst),
    path('doctor_login/', views.doctor_login),
    path('doctor_signup/', views.doctor_signup),

    path('patient_login/', views.patient_login),
    path('patient_register/', views.patient_signup),
]
 