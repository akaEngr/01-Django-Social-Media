from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_User_Model/', views.register_User_Model, name='register_User_Model'),
    path('register_UserCreatioForm/', views.register_UserCreatioForm, name='register_UserCreatioForm'),
    path('register_ModelForm/', views.register_ModelForm, name='register_ModelForm'),
    path('register_manually/', views.register_manually, name='register_manually'),
    
    path('user_login/', views.user_login, name='user_login'),
    path('user_login_manual/', views.user_login_manual, name='user_login_manual'),
    path('user_logout/', views.user_logout, name='user_logout'),
   







]
