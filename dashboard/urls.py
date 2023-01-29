from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('home/', views.d_home),
    path('users/groups', views.d_user_groups),
    path('sondage/', views.sondage),
    path('new_analyse/', views.new_analyse),
    path('list_analyse/', views.list_analyses),
    path('user_lists/', views.user_list),
    path('user_profile/', views.user_profile),
    path('user_profile_security/', views.user_profile_security),
    path('approve_doctor/', views.approve_doctor),
    path('deny_doctor/', views.deny_doctor),
    path('cardio_test/', views.test_cardio)
]
