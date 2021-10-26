from typing import Any, Optional

from django.db import models
from .forms import MyPasswordChangeForm, MyUserProfileEditForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')


class MyEditProfileDataView(UpdateView):
    form_class = MyUserProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def get_object(self) -> models.Model:
        return self.request.user


def RedirectToMyPasswordChangeView(_):
    return redirect('members_settings_password')


class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('members_settings_password_change_done')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super(MyPasswordChangeView, self).get(request, *args, **kwargs)


def MyPasswordChangeDoneView(request):
    return render(request, 'registration/change_password_done.html', {})