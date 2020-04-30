from django.urls import path, include
from Users import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('UpdateProfile/', views.UpdateProfile, name='UpdateProfile'),

]