from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from main.models import Profile

from .forms import UserEditForm, UserForm


class RegisterUser(CreateView):
    form_class = UserForm
    template_name = 'register.html'
    success_url = '/'


class LoginUser(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/'


class UserLogout(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'
    success_url_allowed_hosts = ('account:main_page',)


class UserDetail(DetailView):
    model = Profile
    context_object_name = 'user'
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['form'] = UserEditForm(instance=self.request.user)
        return context

    def get_object(self):
        user = self.request.user
        return user

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
        return render(request, self.template_name, {'form': form})


class ChangePassword(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('account:profile')
