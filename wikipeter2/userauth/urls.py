from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import MyEditProfileDataView, MyPasswordChangeDoneView, MyPasswordChangeView, RedirectToMyPasswordChangeView, UserRegisterView
from .forms import LoginForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form = LoginForm), name='login'),
    path('register-new-user/', UserRegisterView.as_view(), name='register'),
    path('settings/profile', MyEditProfileDataView.as_view(), name='members_settings_profile'),
    path('password/', RedirectToMyPasswordChangeView, name='password'),
    path('settings/password', MyPasswordChangeView.as_view(), name='members_settings_password'),
    path('settings/password_change_done', MyPasswordChangeDoneView, name='members_settings_password_change_done'),
]
